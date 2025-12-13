import asyncio
import sys
import os
import logging
from sqlmodel import Session, select

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import engine, init_db
from app.models.recall import RawRecall
from app.ingestors.rss import RSSIngestor
from app.services.processor import RecallProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def full_pipeline():
    # 1. Init DB (Fresh start if deleted)
    init_db()
    
    # 2. Ingest Real Data (Google News India)
    rss_url = "https://news.google.com/rss/search?q=product+recall+india+when:7d&hl=en-IN&gl=IN&ceid=IN:en"
    ingestor = RSSIngestor(feed_url=rss_url, source_name="GoogleNews-IN")
    
    logger.info("Fetching RSS Feed...")
    items = await ingestor.fetch_latest()
    logger.info(f"Fetched {len(items)} items.")
    
    # 3. Save Raw Recalls
    with Session(engine) as session:
        for item in items:
            import json
            import hashlib
            
            payload_str = json.dumps(item)
            source_id = hashlib.md5(payload_str.encode()).hexdigest()
            
            existing = session.exec(select(RawRecall).where(RawRecall.source_id == source_id)).first()
            if not existing:
                raw = RawRecall(
                    source_id=source_id,
                    source_type="NEWS",
                    raw_payload=payload_str
                )
                session.add(raw)
        session.commit()
    
    logger.info("Raw Data Saved.")

    # 4. Process into Canonical Recalls
    logger.info("Running Processor...")
    processor = RecallProcessor()
    count = await processor.process_raw_recalls(limit=100)
    logger.info(f"Successfully processed {count} new recalls.")

if __name__ == "__main__":
    asyncio.run(full_pipeline())
