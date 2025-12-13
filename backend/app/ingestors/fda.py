from typing import List, Dict, Any
import httpx
import logging
from app.ingestors.base import BaseIngestor
from app.core.constants import SourceType

logger = logging.getLogger(__name__)

class FDAIngestor(BaseIngestor):
    # Food enforcement endpoint
    BASE_URL = "https://api.fda.gov/food/enforcement.json"

    def __init__(self):
        super().__init__(SourceType.GOVT)

    async def fetch_latest(self) -> List[Dict[str, Any]]:
        # OpenFDA supports 'search' and 'limit'
        # Fetch recent enforcements (Recall Initiation Date sorted desc)
        params = {
            "search": "status:Ongoing", # Only active recalls
            "sort": "report_date:desc",
            "limit": 50
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.get(self.BASE_URL, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # OpenFDA returns { meta: ..., results: [...] }
            return data.get("results", [])
