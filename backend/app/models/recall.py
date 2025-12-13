from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.core.constants import Region, ConfidenceLevel, SourceType

class RecallBase(SQLModel):
    title: str
    brand: Optional[str] = None
    product: Optional[str] = None
    category: Optional[str] = None
    region: Region = Region.UNKNOWN
    hazard_summary: Optional[str] = None
    official_action: Optional[str] = None
    confidence_level: ConfidenceLevel = ConfidenceLevel.WATCH
    signal_type: Optional[str] = None # India-specific: "Sample Failure", "Regulatory Action", etc.
    url: Optional[str] = None
    published_date: Optional[datetime] = None # The actual date of the news/recall

class Recall(RecallBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    sources: List["RecallSource"] = Relationship(back_populates="recall")

class RecallSource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    recall_id: Optional[int] = Field(default=None, foreign_key="recall.id")
    source_type: SourceType
    url: str
    title: str
    published_at: Optional[datetime] = None
    
    recall: Optional[Recall] = Relationship(back_populates="sources")

class RawRecall(SQLModel, table=True):
    """Raw ingestion payload before normalization"""
    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: str = Field(index=True) # Unique ID from source (e.g., CPSC ID)
    source_type: SourceType
    raw_payload: str # JSON string
    ingested_at: datetime = Field(default_factory=datetime.utcnow)
