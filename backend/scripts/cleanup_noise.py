import sys
import os
import logging
from sqlmodel import Session, select, delete
# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import engine
from app.models.recall import Recall

# Configure Logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def cleanup_noise():
    print("🧹 Cleaning up noisy records...")
    
    noise_keywords = [
        "funding alert", "raised", "series a", "series b", "series c", "bags $", "mn round", # Finance
        "reviewed", "review:", "tested and reviewed", "best medical alert", "top 10", "buying guide", # Reviews
        "how it works", "how to", "feature update", "eligible for this", "watch face", "ios", "android" # Tech
    ]
    
    deleted_count = 0
    
    with Session(engine) as session:
        # Fetch all recalls to check titles (SQLite ILIKE is tricky, so python filter is safer for script)
        recalls = session.exec(select(Recall)).all()
        
        for r in recalls:
            title_lower = r.title.lower()
            if any(nk in title_lower for nk in noise_keywords):
                print(f"❌ Deleting: {r.title}")
                session.delete(r)
                deleted_count += 1
        
        session.commit()
    
    print(f"✅ Deleted {deleted_count} noisy records.")

if __name__ == "__main__":
    cleanup_noise()
