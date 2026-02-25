from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.user import Watchlist, User
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Watchlist])
def read_watchlists(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Watchlist).where(Watchlist.user_id == current_user.id)
    return session.exec(statement).all()

@router.post("/", response_model=Watchlist)
def create_watchlist(
    watchlist: Watchlist, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    watchlist.user_id = current_user.id
    
    # Check duplicate
    existing = session.exec(
        select(Watchlist)
        .where(Watchlist.user_id == current_user.id)
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
def delete_watchlist(
    id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    watchlist = session.get(Watchlist, id)
    if not watchlist or watchlist.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    
    session.delete(watchlist)
    session.commit()
    return {"ok": True}
