import os
from dotenv import load_dotenv

# Force load from root .env file
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), ".env"))

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.subscription import PushSubscription
from pydantic import BaseModel

router = APIRouter()

# VAPID Keys from environment variables
VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY", "")

class SubscriptionRequest(BaseModel):
    endpoint: str
    keys: dict
    user_id: int

@router.get("/vapid-public-key")
def get_vapid_key():
    if not VAPID_PUBLIC_KEY:
        raise HTTPException(status_code=503, detail="Push notifications not configured")
    return {"publicKey": VAPID_PUBLIC_KEY}

@router.post("/subscribe")
def subscribe(req: SubscriptionRequest, session: Session = Depends(get_session)):
    # Check if exists
    existing = session.exec(select(PushSubscription).where(PushSubscription.endpoint == req.endpoint)).first()
    if existing:
        return {"status": "exists"}
    
    sub = PushSubscription(
        user_id=req.user_id,
        endpoint=req.endpoint,
        p256dh=req.keys['p256dh'],
        auth=req.keys['auth']
    )
    session.add(sub)
    session.commit()
    return {"status": "ok"}
