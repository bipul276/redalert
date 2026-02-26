import sys
import os
import logging
import asyncio
from sqlmodel import Session, delete

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.core.database import engine
from app.models.recall import Recall, RecallSource, RawRecall
from app.services.scheduler_service import run_ingestion_cycle

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def hard_reset():
    logger.info("🧨 WARNING: Performing a HARD RESET of the database...")
    with Session(engine) as session:
        # Delete sources first (foreign key)
        logger.info("Wiping RecallSource...")
        session.exec(delete(RecallSource))
        
        # Delete canonical recalls
        logger.info("Wiping Recall...")
        session.exec(delete(Recall))
        
        # Delete raw payloads
        logger.info("Wiping RawRecall...")
        session.exec(delete(RawRecall))
        
        session.commit()
        logger.info("✅ All existing data (Raw and Canonical) has been WIPED.")
        
    logger.info("⚙️ Starting fresh ingestion cycle...")
    try:
        await run_ingestion_cycle()
        logger.info("✅ Hard reset and fresh ingestion complete!")
    except Exception as e:
        logger.error(f"❌ Error during fresh ingestion: {e}")

if __name__ == "__main__":
    asyncio.run(hard_reset())
