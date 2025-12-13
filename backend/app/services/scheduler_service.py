import logging
from sqlmodel import Session, select
import hashlib
import json

from app.core.database import engine
from app.models.recall import RawRecall
from app.ingestors.rss import RSSIngestor
from app.services.processor import RecallProcessor

logger = logging.getLogger(__name__)

async def run_ingestion_cycle():
    """
    Runs the full ingestion pipeline:
    1. Fetch RSS Feeds (India/US)
    2. Save Raw Data (Deduplicated)
    3. Process Raw Data into Canonical Recalls
    """
    logger.info("⏳ Starting Scheduled Ingestion Cycle...")
    
    # 1. Define Sources
    sources = [
        # Broad India Sources
        ("https://news.google.com/rss/search?q=product+recall+india+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-General"),
        # Regulatory & Specific Signals
        ("https://news.google.com/rss/search?q=FSSAI+unsafe+sample+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-FSSAI"),
        ("https://news.google.com/rss/search?q=food+safety+sample+failed+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-FoodSafety"),
        ("https://news.google.com/rss/search?q=CDSCO+alert+drug+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-CDSCO"),
        ("https://news.google.com/rss/search?q=drug+licence+cancelled+india+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-Pharma"),
        ("https://news.google.com/rss/search?q=food+safety+seizure+india+when:15d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-Seizure"),
        ("https://news.google.com/rss/search?q=WHO+medical+product+alert+India+when:30d&hl=en-IN&gl=IN&ceid=IN:en", "GoogleNews-IN-WHO"),
        
        # US Source (Unchanged)
        ("https://news.google.com/rss/search?q=product+recall+usa+when:7d&hl=en-US&gl=US&ceid=US:en", "GoogleNews-US")
    ]
    
    total_fetched = 0
    
    # 2. Fetch & Save Raw
    with Session(engine) as session:
        for url, source_name in sources:
            try:
                ingestor = RSSIngestor(feed_url=url, source_name=source_name)
                items = await ingestor.fetch_latest()
                total_fetched += len(items)
                
                for item in items:
                    # Inject Source Origin for Processor
                    item["_source_origin"] = source_name
                    
                    payload_str = json.dumps(item)
                    source_id = hashlib.md5(payload_str.encode()).hexdigest()
                    
                    # Deduplication Check
                    existing = session.exec(select(RawRecall).where(RawRecall.source_id == source_id)).first()
                    if not existing:
                        raw = RawRecall(
                            source_id=source_id,
                            source_type="NEWS",
                            raw_payload=payload_str
                        )
                        session.add(raw)
                
                session.commit()
            except Exception as e:
                logger.error(f"Error ingesting {source_name}: {e}")
                
    logger.info(f"✅ Fetched and saved {total_fetched} potential recalls.")

    # 3. Process into Canonical Recalls
    try:
        processor = RecallProcessor()
        count = await processor.process_raw_recalls(limit=500) # Process larger batch for initial load
        logger.info(f"✅ Processed {count} new canonical recalls.")
    except Exception as e:
        logger.error(f"Error processing recalls: {e}")
        
    logger.info("🏁 Ingestion Cycle Complete.")
