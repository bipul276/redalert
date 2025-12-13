from typing import List, Dict, Any
from datetime import datetime, timedelta
import httpx
import logging
from app.ingestors.base import BaseIngestor
from app.core.constants import SourceType

logger = logging.getLogger(__name__)

class CPSCIngestor(BaseIngestor):
    BASE_URL = "https://www.saferproducts.gov/RestWebServices/Recall"

    def __init__(self):
        super().__init__(SourceType.GOVT)

    async def fetch_latest(self) -> List[Dict[str, Any]]:
        # Fetch last 90 days by default for MVP
        start_date = (datetime.utcnow() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        params = {
            "Format": "json",
            "RecallDateStart": start_date
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # CPSC returns a list directly or wrapped? 
            # Usually strict list in JSON format from SaferProducts
            return data if isinstance(data, list) else []

    def normalize(self, raw_item: Dict[str, Any]):
        # TODO: Implement normalization logic in Phase 2
        pass
