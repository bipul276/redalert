from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.subscription import PushSubscription
from pydantic import BaseModel

router = APIRouter()

# MVP VAPID Keys (Generated for this session)
# In production -> ENV VARS
VAPID_PUBLIC_KEY = "BK0s_q_R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a-R_a"
# Note: Real VAPID generation is needed. I will use a valid format below.
VAPID_PUBLIC_KEY = "BEl62iUYgUivxIkv69yViEuiBIa-Ib9-SkvMeAtA3LFgDzkrxZJjSgSnfckjBJuBkr3qBUYIuQRWV_Hw8a6E4DM"
VAPID_PRIVATE_KEY = "PREDEFINED_PRIVATE_KEY_WILL_BE_SET_IN_NOTIFIER" 
# Ideally, we don't expose private key here, just need public for frontend.

class SubscriptionRequest(BaseModel):
    endpoint: str
    keys: dict
    user_id: int # Hardcoded for MVP

@router.get("/vapid-public-key")
def get_vapid_key():
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
