import logging
import json
import html
import re
from typing import List, Optional
from sqlmodel import Session, select
from app.core.database import engine
from app.models.recall import RawRecall, Recall, RecallSource
from app.nlp.engine import NLPEngine
from app.scoring.confidence import ConfidenceScorer
from app.core.constants import Region, ConfidenceLevel
from datetime import datetime

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
                    
                    # Unified Field extraction
                    raw_title = payload.get("title", "Unknown Title")
                    title = html.unescape(raw_title) # Fix &nbsp; and others
                    
                    raw_desc = payload.get("summary", "") or payload.get("description", "")
                    
                    def strip_tags(html_text):
                        return re.sub(r'<[^>]+>', '', html_text)

                    desc = strip_tags(html.unescape(raw_desc))
                    
                    # Combine text for NLP
                    full_text = f"{title} {desc}"
                    lower_full_text = full_text.lower()
                    
                    # NOISE FILTER (Explicit exclusion)
                    noise_keywords = [
                        "funding alert", "raised", "series a", "series b", "series c", "bags $", "mn round", # Finance
                        "reviewed", "review:", "tested and reviewed", "best medical alert", "top 10", "buying guide", # Reviews
                        "how it works", "how to", "feature update", "eligible for this", "watch face", "ios", "android" # Tech Tutorials
                    ]
                    
                    if any(nk in lower_full_text for nk in noise_keywords):
                        logger.info(f"🗑️ Skipped Noise: {title}")
                        continue

                    # 2. NLP Analysis
                    analysis = NLPEngine.analyze_text(full_text)
                    # Extract entities (basic regex from NLP engine)
                    analysis["entities"] = NLPEngine.extract_entity_candidates(full_text)
                    
                    # 3. Signals & Region Logic
                    source_origin = payload.get("_source_origin", "")
                    is_india_source = "IN" in source_origin or "India" in source_origin
                    
                    # Foreign Exclusion Logic
                    foreign_keywords = [
                        "usa", "u.s.", "united states", "canada", "ontario", "toronto", "vancouver", "montreal",
                        "nigeria", "africa", "japan", "australia", "sydney", "melbourne", "brisbane",
                        "uk", "united kingdom", "london", "dublin", "ireland", "new zealand", "europe",
                        "fda", "cpsc", "hsa", "singapore", "tga", "california", "texas",
                        "venezuela", "maduro", "white house", "sanctions", "oil tanker", "shipping firms",
                        "russia", "ukraine", "war", "military", "army", "navy", "air force", "troops", "deployed"
                    ]
                    
                    has_foreign_mention = any(fk in lower_full_text for fk in foreign_keywords)
                    
                    if (analysis["is_india"] or is_india_source) and not has_foreign_mention:
                        region = Region.IN
                    else:
                        region = Region.US
                    
                    # Signal Logic (India Specific)
                    signal_type = None
                    confidence = ConfidenceLevel.WATCH # Default

                    # US Defaults
                    if region == Region.US:
                         score = ConfidenceScorer.calculate_score(raw.source_type, analysis)
                         confidence = ConfidenceScorer.get_bucket(score)
                    else:
                        # INDIA SIGNAL LADDER
                        lower_text = full_text.lower()
                        
                        # A. Define Signals
                        if any(k in lower_text for k in ["ban", "banned", "cancelled", "suspended", "seized", "ordered to withdraw"]):
                            signal_type = "Regulatory Action"
                        elif any(k in lower_text for k in ["sample failed", "substandard", "not of standard quality", "adulterated", "unsafe"]):
                            signal_type = "Sample Failure"
                        elif any(k in lower_text for k in ["probe", "investigation", "complaint", "show cause"]):
                            signal_type = "Investigation"
                        elif "recall" in lower_text:
                            signal_type = "Recall"
                        
                        # B. Assign Confidence based on Signal
                        if signal_type == "Regulatory Action":
                            confidence = ConfidenceLevel.CONFIRMED
                        elif signal_type == "Sample Failure":
                            confidence = ConfidenceLevel.PROBABLE
                        elif signal_type == "Recall": 
                             confidence = ConfidenceLevel.CONFIRMED
                        else:
                            # Investigations or weak signals -> Watch
                             signal_type = signal_type or "Investigation" # Default
                             confidence = ConfidenceLevel.WATCH
                    
                    # 4. Create Canonical Recall
                    # Fuzzy Deduplication (MVP)
                    candidates = session.exec(select(Recall).where(Recall.region == region)).all()
                    
                    from difflib import SequenceMatcher
                    
                    existing_recall = None
                    for cand in candidates:
                        ratio = SequenceMatcher(None, title.lower(), cand.title.lower()).ratio()
                        if ratio > 0.65: # Threshold
                            existing_recall = cand
                            break
                    
                    from email.utils import parsedate_to_datetime
                    
                    # Date Extraction
                    pub_date = None
                    raw_date = payload.get("published") or payload.get("pubDate") or payload.get("date") or payload.get("published_at")
                    
                    if raw_date:
                        try:
                            # Try ISO first (common in JSON APIs)
                            pub_date = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                        except ValueError:
                            try:
                                # Try RSS/Email format (common in Feedparser)
                                pub_date = parsedate_to_datetime(raw_date)
                            except Exception:
                                logger.warning(f"Could not parse date: {raw_date}")
                                pub_date = None

                    if existing_recall:
                        # MERGE: Add as new source to existing recall
                        existing_source = session.exec(select(RecallSource).where(RecallSource.recall_id == existing_recall.id).where(RecallSource.url == payload.get("link"))).first()
                        if not existing_source:
                            source = RecallSource(
                                recall_id=existing_recall.id,
                                source_type=raw.source_type,
                                url=payload.get("link", payload.get("url", "#")),
                                title=title
                            )
                            session.add(source)
                            logger.info(f"Merged duplicate into Recall {existing_recall.id}: {title}")
                    else:
                        # CREATE NEW
                        recall = Recall(
                            title=title,
                            hazard_summary=desc[:500],
                            region=region,
                            confidence_level=confidence,
                            signal_type=signal_type, 
                            brand=analysis["entities"][0] if analysis["entities"] else None,
                            url=payload.get("link", payload.get("url", "#")),
                            published_date=pub_date
                        )
                        session.add(recall)
                        session.commit()
                        session.refresh(recall)
                        
                        source = RecallSource(
                            recall_id=recall.id,
                            source_type=raw.source_type,
                            url=payload.get("link", payload.get("url", "#")),
                            title=title
                        )
                        session.add(source)
                        processed_count += 1
                        logger.info(f"Created Recall: {title} [{confidence}] Signal: {signal_type}")

                        # 6. MATCHING ENGINE
                        await self.check_matches(session, recall)
                    
                except Exception as e:
                    logger.error(f"Failed to process RawRecall {raw.id}: {e}")
            
            session.commit()
            return processed_count

    async def check_matches(self, session: Session, recall: Recall):
        from app.models.user import Watchlist
        from app.services.notifier import notifier
        from app.models.user import User
        
        watchlists = session.exec(select(Watchlist)).all()
        
        for w in watchlists:
            match = False
            if w.type == "BRAND" and recall.brand and w.value.lower() in recall.brand.lower():
                match = True
            elif w.type == "PRODUCT" and w.value.lower() in recall.title.lower():
                match = True
                
            if match:
                logger.info(f"!!! ALERT TRIGGERED !!! User {w.user_id} matched '{w.value}' in Recall '{recall.title}'")
                
                user = session.get(User, w.user_id)
                if user:
                    await notifier.notify_user_alert(user, recall.title, w.value)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    import asyncio
    processor = RecallProcessor()
    count = asyncio.run(processor.process_raw_recalls())
    print(f"Processed {count} new canonical recalls.")
