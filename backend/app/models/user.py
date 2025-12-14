from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    
    # 2FA & Security
    totp_secret_enc: Optional[str] = None # Encrypted
    recovery_codes: Optional[str] = None # JSON list of hashed codes
    
    # Rate Limiting / Lockout
    failed_login_attempts: int = Field(default=0)
    last_failed_login: Optional[datetime] = None
    locked_until: Optional[datetime] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    watchlists: List["Watchlist"] = Relationship(back_populates="user")

class Watchlist(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    
    # Type of watch: "BRAND", "CATEGORY", "PRODUCT", "REGION"
    type: str 
    # Value to match: "Tesla", "Baby Food", "US"
    value: str 
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user: Optional[User] = Relationship(back_populates="watchlists")
