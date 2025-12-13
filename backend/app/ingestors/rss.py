from typing import List, Dict, Any
import httpx
import xml.etree.ElementTree as ET
import logging
from app.ingestors.base import BaseIngestor
from app.core.constants import SourceType

logger = logging.getLogger(__name__)

class RSSIngestor(BaseIngestor):
    def __init__(self, feed_url: str, source_name: str = "RSS"):
        super().__init__(SourceType.NEWS)
        self.feed_url = feed_url
        self.source_name = source_name

    async def fetch_latest(self) -> List[Dict[str, Any]]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.feed_url, timeout=30.0)
                response.raise_for_status()
                content = response.content

            root = ET.fromstring(content)
            items = []
            
            # Navigate standard RSS 2.0 structure: channel -> item
            channel = root.find("channel")
            if channel is None:
                # Some feeds might be Atom, but Google News is typically RSS 2.0
                return []

            for item in channel.findall("item"):
                title = item.find("title").text if item.find("title") is not None else ""
                link = item.find("link").text if item.find("link") is not None else ""
                pubDate = item.find("pubDate").text if item.find("pubDate") is not None else ""
                description = item.find("description").text if item.find("description") is not None else ""
                
                items.append({
                    "title": title,
                    "link": link,
                    "published": pubDate,
                    "summary": description,
                    "source_name": self.source_name
                })
            
            return items
        except Exception as e:
            logger.error(f"Failed to fetch RSS from {self.feed_url}: {e}")
            return []
