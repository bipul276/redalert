import asyncio
import logging
from sqlmodel import Session, select
from app.core.database import engine, init_db
from app.models.recall import RawRecall
from app.ingestors.rss import RSSIngestor

async def run_ingestion():
    logger.info("Starting Batch Ingestion Job")
    
    # Initialize Ingestors
    ingestors = [
        CPSCIngestor(),
        FDAIngestor(),
        NHTSAIngestor(),
        # India Signals (Phase 3)
        RSSIngestor(
            feed_url="https://news.google.com/rss/search?q=product+recall+india+when:7d&hl=en-IN&gl=IN&ceid=IN:en",
            source_name="GoogleNews-IN"
        ),
        RSSIngestor(
            feed_url="https://news.google.com/rss/search?q=fssai+alert+india&hl=en-IN&gl=IN&ceid=IN:en",
            source_name="GoogleNews-FSSAI"
        )
    ]
    
    # Create DB tables if not exist
    init_db()
    
    with Session(engine) as session:
        for ingestor in ingestors:
            try:
                items = await ingestor.run()
                logger.info(f"Saving {len(items)} items from {ingestor.source_type}")
                
                count_new = 0
                for item in items:
                    # TODO: Extract robust ID. For now using entire payload hash or specific ID if known
                    # Phase 2 will handle distinct IDs. Phase 1 is Raw Dump.
                    # We just dump everything as raw payload for now.
                    
                    # Rudimentary dedup by source_id check (if we had one)
                    # For MVP Phase 1: Just insert (or efficient check)
                    
                    # Assuming we dump generic JSON
                    import json
                    payload_str = json.dumps(item)
                    
                    # Create RawRecall
                    # Note: We need a unique source_id from the item.
                    # CPSC: RecallID? FDA: EventID?
                    # For now using a hash of payload as source_id to avoid crash
                    import hashlib
                    source_id = hashlib.md5(payload_str.encode()).hexdigest()
                    
                    # Check existing
                    existing = session.exec(select(RawRecall).where(RawRecall.source_id == source_id)).first()
                    if not existing:
                        db_item = ingestor.create_raw_recall(source_id, payload_str)
                        session.add(db_item)
                        count_new += 1
                
                session.commit()
                logger.info(f"Saved {count_new} new items for {ingestor.source_type}")
                
            except Exception as e:
                logger.error(f"Ingestion cycle failed for {ingestor.source_type}: {e}")

if __name__ == "__main__":
    asyncio.run(run_ingestion())
