from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime
import logging
from app.models.recall import RawRecall
from app.core.constants import SourceType

logger = logging.getLogger(__name__)

class BaseIngestor(ABC):
    def __init__(self, source_type: SourceType):
        self.source_type = source_type

    @abstractmethod
    async def fetch_latest(self) -> List[Dict[str, Any]]:
        """Fetch raw data from the source (API/RSS). Returns list of Dicts."""
        pass

    def create_raw_recall(self, source_id: str, payload: str) -> RawRecall:
        """Helper to create a RawRecall model"""
        return RawRecall(
            source_id=source_id,
            source_type=self.source_type,
            raw_payload=payload,
            ingested_at=datetime.utcnow()
        )

    async def run(self):
        """Main execution method"""
        logger.info(f"Starting ingestion for {self.source_type}")
        try:
            items = await self.fetch_latest()
            logger.info(f"Fetched {len(items)} items from {self.source_type}")
            # In a real app, we would save these to DB here
            return items
        except Exception as e:
            logger.error(f"Ingestion failed for {self.source_type}: {e}")
            raise
