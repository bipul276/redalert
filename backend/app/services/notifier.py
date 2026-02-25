import os
import logging
import json
from abc import ABC, abstractmethod
from app.models.user import User
from sqlmodel import Session, select
from app.core.database import engine
from app.models.subscription import PushSubscription

logger = logging.getLogger(__name__)

# VAPID Keys from environment
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY", "")
VAPID_CLAIMS = {
    "sub": os.getenv("VAPID_MAILTO", "mailto:admin@redalert.example.com")
}

class BaseNotificationProvider(ABC):
    @abstractmethod
    async def send_email(self, recipient_email: str, subject: str, content: str):
        pass

class LogEmailProvider(BaseNotificationProvider):
    async def send_email(self, recipient_email: str, subject: str, content: str):
        logger.info(f"--- [MOCK EMAIL SENT] ---")
        logger.info(f"To: {recipient_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {content}")
        return True

class NotificationService:
    def __init__(self, provider: BaseNotificationProvider = None):
        self.provider = provider or LogEmailProvider()

    async def notify_user_alert(self, user: User, recall_title: str, match_keyword: str):
        # 1. Email
        subject = f"🔴 RedAlert: New recall for '{match_keyword}'"
        content = f"Recall matched: {recall_title}"
        await self.provider.send_email(user.email, subject, content)
        
        # 2. WebPush
        self.send_webpush(user.id, recall_title)

    def send_webpush(self, user_id: int, message: str):
        if not VAPID_PRIVATE_KEY or not VAPID_PUBLIC_KEY:
            logger.warning("VAPID keys not configured — skipping push notification")
            return
            
        try:
            from pywebpush import webpush, WebPushException
            
            with Session(engine) as session:
                subs = session.exec(select(PushSubscription).where(PushSubscription.user_id == user_id)).all()
                for sub in subs:
                    try:
                        webpush(
                            subscription_info={
                                "endpoint": sub.endpoint,
                                "keys": {
                                    "p256dh": sub.p256dh,
                                    "auth": sub.auth
                                }
                            },
                            data=json.dumps({"title": "RedAlert", "body": message}),
                            vapid_private_key=VAPID_PRIVATE_KEY,
                            vapid_claims=VAPID_CLAIMS
                        )
                        logger.info(f"Push sent to {sub.id}")
                    except WebPushException as ex:
                        logger.error(f"WebPush failed: {ex}")
                    except Exception as e:
                        logger.warning(f"Push error: {e}")
        except ImportError:
            logger.warning("pywebpush not installed — skipping push notifications")
        except Exception as outer_e:
            logger.error(f"Push db error: {outer_e}")

# Singleton Instance
notifier = NotificationService()
