from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class PushSubscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    
    endpoint: str = Field(index=True)
    p256dh: str
    auth: str
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
