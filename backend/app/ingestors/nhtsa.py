from typing import List, Dict, Any
from datetime import datetime
import httpx
import logging
from app.ingestors.base import BaseIngestor
from app.core.constants import SourceType

logger = logging.getLogger(__name__)

class NHTSAIngestor(BaseIngestor):
    # NHTSA Recall Query API
    BASE_URL = "https://api.nhtsa.gov/recalls/recallquery"

    def __init__(self):
        super().__init__(SourceType.GOVT)

    async def fetch_latest(self) -> List[Dict[str, Any]]:
        # Strategy: Fetch recalls for current and previous year
        # This covers most relevant active recalls
        years = [datetime.now().year, datetime.now().year - 1]
        all_recalls = []
        
        async with httpx.AsyncClient() as client:
            for year in years:
                try:
                    params = {"modelyear": str(year), "format": "json"}
                    response = await client.get(self.BASE_URL, params=params, timeout=30.0)
                    response.raise_for_status()
                    data = response.json()
                    
                    # NHTSA returns { Count: ..., Message: ..., Results: [...] }
                    results = data.get("Results", [])
                    all_recalls.extend(results)
                except Exception as e:
                    logger.error(f"Failed to fetch NHTSA recalls for year {year}: {e}")
        
        return all_recalls
