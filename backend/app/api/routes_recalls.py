from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.recall import Recall, RecallSource
from app.core.constants import Region, ConfidenceLevel

router = APIRouter()

from datetime import date, timedelta, datetime

@router.get("/", response_model=List[Recall])
def read_recalls(
    region: Optional[Region] = None, 
    q: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    status: Optional[List[str]] = Query(None),
    signal_type: Optional[List[str]] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    session: Session = Depends(get_session)
):
    statement = select(Recall)
    
    if region:
        statement = statement.where(Recall.region == region)
        
    if q:
        statement = statement.where(Recall.title.ilike(f"%{q}%"))

    if start_date:
        statement = statement.where(Recall.created_at >= start_date)
        
    if end_date:
        next_day = end_date + timedelta(days=1)
        statement = statement.where(Recall.created_at < next_day)

    if status:
        statement = statement.where(Recall.confidence_level.in_(status))

    if signal_type:
        statement = statement.where(Recall.signal_type.in_(signal_type))
    
    # Always sort by newest first
    statement = statement.order_by(Recall.id.desc())
    
    # Pagination
    statement = statement.offset(offset).limit(limit)
        
    return session.exec(statement).all()

@router.get("/{id}", response_model=Recall)
def read_recall(id: int, session: Session = Depends(get_session)):
    recall = session.get(Recall, id)
    if not recall:
        raise HTTPException(status_code=404, detail="Recall not found")
    return recall
