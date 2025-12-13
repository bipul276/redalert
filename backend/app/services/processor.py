import logging
import json
from typing import List, Optional
from sqlmodel import Session, select
from app.core.database import engine
from app.models.recall import RawRecall, Recall, RecallSource
from app.nlp.engine import NLPEngine
from app.scoring.confidence import ConfidenceScorer
from app.core.constants import Region

logger = logging.getLogger(__name__)

class RecallProcessor:
    async def process_raw_recalls(self, limit: int = 50, target_ids: List[int] = None):
        """
        Main loop to process raw ingested data into canonical Recalls.
        In a real app, this would be an async worker or triggered by events.
        """
        processed_count = 0
        
        with Session(engine) as session:
            # Fetch all raw recalls (In MVP, we process everything. Real app needs 'processed' flag)
            statement = select(RawRecall)
            if target_ids:
                statement = statement.where(RawRecall.id.in_(target_ids))
            else:
                statement = statement.limit(limit)
                
            raw_items = session.exec(statement).all()
            
            for raw in raw_items:
                try:
                    # 1. Parse Payload
                    payload = json.loads(raw.raw_payload)
                    
                    # Unified Field extraction (very basic mapping)
                    title = payload.get("title", "Unknown Title")
                    raw_desc = payload.get("summary", "") or payload.get("description", "")
                    
                    import re
                    def strip_tags(html):
                        return re.sub(r'<[^>]+>', '', html)

                    desc = strip_tags(raw_desc)
                    
                    # Combine text for NLP
                    full_text = f"{title} {desc}"
                    
                    # 2. NLP Analysis
                    analysis = NLPEngine.analyze_text(full_text)
                    # Extract entities (basic regex from NLP engine)
                    analysis["entities"] = NLPEngine.extract_entity_candidates(full_text)
                    
                    # 3. Confidence Scoring
                    score = ConfidenceScorer.calculate_score(raw.source_type, analysis)
                    confidence = ConfidenceScorer.get_bucket(score)
                    
                    # 4. Region Logic
                    region = Region.IN if analysis["is_india"] else Region.US # Default to US/Global for now
                    if raw.source_type == "GOV" and "india" not in full_text.lower():
                         # CPSC/NHTSA/FDA are US by default unless specified
                         region = Region.US

                    # 5. Create Canonical Recall
                    # Check duplicate by title (MVP dedup)
                    existing = session.exec(select(Recall).where(Recall.title == title)).first()
                    
                    if not existing:
                        recall = Recall(
                            title=title,
                            hazard_summary=desc[:500], # Truncate for MVP
                            region=region,
                            confidence_level=confidence,
                            brand=analysis["entities"][0] if analysis["entities"] else None,
                            url=payload.get("link", payload.get("url", "#"))
                        )
                        session.add(recall)
                        session.commit()
                        session.refresh(recall)
                        
                        # Add Source Link
                        source = RecallSource(
                            recall_id=recall.id,
                            source_type=raw.source_type,
                            url=payload.get("link", payload.get("url", "#")),
                            title=title
                        )
                        session.add(source)
                        processed_count += 1
                        logger.info(f"Created Recall: {title} [{confidence}]")

                        # 6. MATCHING ENGINE (Phase 5)
                        await self.check_matches(session, recall)
                    
                except Exception as e:
                    logger.error(f"Failed to process RawRecall {raw.id}: {e}")
            
            session.commit()
            return processed_count

    async def check_matches(self, session: Session, recall: Recall):
        from app.models.user import Watchlist
        from app.services.notifier import notifier
        
        # Simple exact match on Brand or loose match on Title
        # 1. Fetch all active watchlists
        # Optimization: In real app, query filtering happen in DB
        watchlists = session.exec(select(Watchlist)).all()
        
        for w in watchlists:
            match = False
            if w.type == "BRAND" and recall.brand and w.value.lower() in recall.brand.lower():
                match = True
            elif w.type == "PRODUCT" and w.value.lower() in recall.title.lower():
                match = True
                
            if match:
                # ALERT TRIGGERED
                logger.info(f"!!! ALERT TRIGGERED !!! User {w.user_id} matched '{w.value}' in Recall '{recall.title}'")
                
                # Fetch user email
                user = session.get(User, w.user_id)
                if user:
                    await notifier.notify_user_alert(user, recall.title, w.value)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    processor = RecallProcessor()
    count = processor.process_raw_recalls()
    print(f"Processed {count} new canonical recalls.")
