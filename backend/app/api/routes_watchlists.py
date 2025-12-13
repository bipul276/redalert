from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import Watchlist, User

router = APIRouter()

# MVP: Hardcoded User ID for Phase 5 initial testing
# In a real app, this comes from `get_current_user` dependency
TEST_USER_ID = 1

@router.get("/", response_model=List[Watchlist])
def read_watchlists(session: Session = Depends(get_session)):
    statement = select(Watchlist).where(Watchlist.user_id == TEST_USER_ID)
    return session.exec(statement).all()

@router.post("/", response_model=Watchlist)
def create_watchlist(watchlist: Watchlist, session: Session = Depends(get_session)):
    # Force user_id for safety in MVP
    watchlist.user_id = TEST_USER_ID
    
    # Check duplicate
    existing = session.exec(
        select(Watchlist)
        .where(Watchlist.user_id == TEST_USER_ID)
        .where(Watchlist.type == watchlist.type)
        .where(Watchlist.value == watchlist.value)
    ).first()
    
    if existing:
        return existing

    session.add(watchlist)
    session.commit()
    session.refresh(watchlist)
    return watchlist

@router.delete("/{id}")
def delete_watchlist(id: int, session: Session = Depends(get_session)):
    watchlist = session.get(Watchlist, id)
    if not watchlist or watchlist.user_id != TEST_USER_ID:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    
    session.delete(watchlist)
    session.commit()
    return {"ok": True}
