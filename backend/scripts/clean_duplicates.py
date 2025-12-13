import sys
import os
import logging
from difflib import SequenceMatcher
from sqlmodel import Session, select

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.core.database import engine
from app.models.recall import Recall, RecallSource

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clean_duplicates():
    print("🧹 Cleaning Duplicates...")
    
    with Session(engine) as session:
        recalls = session.exec(select(Recall)).all()
        # Sort by ID to keep the older one (usually)
        recalls.sort(key=lambda x: x.id)
        
        seen = []
        deleted_count = 0
        
        for r in recalls:
            is_dup = False
            r_text = (r.title + " " + (r.brand or "")).lower()
            
            for params in seen:
                existing_id, existing_title = params
                
                 # Fuzzy Ratio
                ratio = SequenceMatcher(None, r.title.lower(), existing_title.lower()).ratio()
                
                # Check Overlap
                # e.g. "Patanjali Ghee failed" vs "Samples of Patanjali Ghee failed"
                if ratio > 0.65:
                    is_dup = True
                    # MERGE
                    print(f"   Using {existing_id} for {r.id} ({r.title[:30]}...)")
                    
                    # Move Sources
                    sources = session.exec(select(RecallSource).where(RecallSource.recall_id == r.id)).all()
                    for s in sources:
                        s.recall_id = existing_id
                        session.add(s)
                    
                    # Delete Duplicate Recall
                    session.delete(r)
                    deleted_count += 1
                    break
            
            if not is_dup:
                seen.append((r.id, r.title))
        
        session.commit()
        print(f"✅ Merged/Deleted {deleted_count} duplicates.")

if __name__ == "__main__":
    clean_duplicates()
