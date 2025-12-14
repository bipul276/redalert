from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.recall import Recall
from app.core.constants import ConfidenceLevel, Region
from app.api.deps import get_current_admin_user
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class RecallUpdate(BaseModel):
    title: Optional[str] = None
    confidence_level: Optional[ConfidenceLevel] = None
    region: Optional[Region] = None
    hazard_summary: Optional[str] = None
    official_action: Optional[str] = None
    brand: Optional[str] = None

@router.patch("/{id}", response_model=Recall)
def update_recall(
    id: int, 
    recall_update: RecallUpdate, 
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    recall = session.get(Recall, id)
    if not recall:
        raise HTTPException(status_code=404, detail="Recall not found")
    
    recall_data = recall_update.dict(exclude_unset=True)
    for key, value in recall_data.items():
        setattr(recall, key, value)
        
    session.add(recall)
    session.commit()
    session.refresh(recall)
    return recall

@router.delete("/{id}")
def delete_recall(
    id: int, 
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user)
):
    recall = session.get(Recall, id)
    if not recall:
         raise HTTPException(status_code=404, detail="Recall not found")
    
    session.delete(recall)
    session.commit()
    return {"ok": True}
