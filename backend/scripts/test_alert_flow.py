import asyncio
import sys
import os
import json
import logging

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlmodel import Session, select
from app.core.database import engine, init_db
from app.models.user import User, Watchlist
from app.models.recall import RawRecall, Recall
from app.services.processor import RecallProcessor

# Configure logging to see Mock Email
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_alert_flow():
    with Session(engine) as session:
        # 1. Setup Test User
        user = session.exec(select(User).where(User.email == "test@example.com")).first()
        if not user:
            user = User(email="test@example.com", hashed_password="hashed_secret", full_name="Test User")
            session.add(user)
            session.commit()
            session.refresh(user)
            logger.info(f"Created Test User: {user.email} (ID: {user.id})")
        
        # 2. Setup Watchlist
        watchlist = session.exec(select(Watchlist)
            .where(Watchlist.user_id == user.id)
            .where(Watchlist.value == "Toyota")).first()
            
        if not watchlist:
            watchlist = Watchlist(user_id=user.id, type="BRAND", value="Toyota")
            session.add(watchlist)
            session.commit()
            logger.info("Added Watchlist for 'Toyota'")

        # 3. Inject Fake RawRecall
        fake_payload = json.dumps({
            "title": "Toyota recalls 1000 units of Camry for brake issue",
            "summary": "Brake pedal may become stiff.",
            "url": "http://toyota.com/recall",
            "source": "SIMULATED"
        })
        
        # Check if already processed to avoid dup bypass
        # For test, we make title unique
        unique_title = "Toyota recalls 1000 units of Camry for brake issue - TEST " + str(os.urandom(4).hex())
        fake_payload = fake_payload.replace("Toyota recalls 1000 units of Camry for brake issue", unique_title)
        
        raw = RawRecall(
            source_id="test_" + os.urandom(4).hex(),
            source_type="NEWS",
            raw_payload=fake_payload
        )
        session.add(raw)
        session.commit()
        session.refresh(raw)
        raw_id = raw.id
        logger.info(f"Injected RawRecall: {unique_title} (ID: {raw_id})")

    # 4. Run Processor
    processor = RecallProcessor()
    logger.info(f"Running Processor for RawRecall ID: {raw_id}...")
    processed = await processor.process_raw_recalls(target_ids=[raw_id])
    
    logger.info(f"Processed count: {processed}")

if __name__ == "__main__":
    asyncio.run(test_alert_flow())
