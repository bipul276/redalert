import sys
import os
import logging
import asyncio
from sqlmodel import Session, select, delete

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import engine
from app.models.recall import Recall, RecallSource, RawRecall
from app.services.processor import RecallProcessor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def rebuild_data():
    logger.info("🧹 Step 1: Clearing all existing canonical recalls...")
    with Session(engine) as session:
        # Delete sources first (foreign key)
        session.exec(delete(RecallSource))
        # Delete recalls
        session.exec(delete(Recall))
        session.commit()
        logger.info("✅ Cleared canonical recalls.")
        
        # Check raw recalls count
        raw_count = session.exec(select(RawRecall)).all()
        logger.info(f"📦 Found {len(raw_count)} Raw Recalls ready for processing.")

    logger.info("⚙️ Step 2: Reprocessing all Raw Recalls with updated NLP logic...")
    processor = RecallProcessor()
    # Process up to 5000 to ensure everything existing is handled
    processed_count = await processor.process_raw_recalls(limit=5000)
    
    logger.info(f"✅ Rebuild complete! Generated {processed_count} new clean canonical recalls.")

if __name__ == "__main__":
    asyncio.run(rebuild_data())
