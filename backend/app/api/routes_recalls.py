from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.recall import Recall, RecallSource
from app.core.constants import Region, ConfidenceLevel

router = APIRouter()

@router.get("/", response_model=List[Recall])
def read_recalls(
    region: Optional[Region] = None, 
    q: Optional[str] = None,
    session: Session = Depends(get_session)
):
    statement = select(Recall)
    
    if region:
        statement = statement.where(Recall.region == region)
        
    if q:
        # Basic case-insensitive search
        statement = statement.where(Recall.title.ilike(f"%{q}%"))
    
    # Always sort by newest first (descending ID/date)
    statement = statement.order_by(Recall.id.desc())
        
    return session.exec(statement).all()

@router.get("/{id}", response_model=Recall)
def read_recall(id: int, session: Session = Depends(get_session)):
    recall = session.get(Recall, id)
    if not recall:
        raise HTTPException(status_code=404, detail="Recall not found")
    return recall
