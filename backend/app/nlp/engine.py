import re
from typing import Dict, Any

class NLPEngine:
    # 5.1 Stage 1: Recall Intent Keywords
    RECALL_KEYWORDS = {
        "recall", "withdrawn", "safety alert", "manufacturing defect", 
        "hazard", "batch issue", "consumer warning", "stop use", 
        "fire risk", "choking hazard", "contamination"
    }

    # 5.3 Stage 3: Region Applicability
    INDIA_KEYWORDS = {
        "india", "indian", "delhi", "mumbai", "bangalore", "fssai", 
        "bis", "morth", "dgca", "rupee", "rs."
    }

    @classmethod
    def analyze_text(cls, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # 1. Intent Detection
        intent_score = 0
        found_keywords = []
        for kw in cls.RECALL_KEYWORDS:
            if kw in text_lower:
                intent_score += 1
                found_keywords.append(kw)
        
        is_recall = intent_score > 0 # Hard gate: must have at least one keyword

        # 2. Region Detection
        region_score = 0
        for kw in cls.INDIA_KEYWORDS:
            if kw in text_lower:
                region_score += 1
        
        is_india = region_score > 0 

        return {
            "is_recall": is_recall,
            "intent_score": intent_score,
            "intent_keywords": found_keywords,
            "is_india": is_india,
            "region_score": region_score
        }

    @classmethod
    def extract_entity_candidates(cls, text: str):
        # Very basic regex for capitalized words (potential brands) - Stage 2 (Lite)
        # In a real app, this would be spaCy.
        # Captures "Brand Name" distinct from start of sentences
        return list(set(re.findall(r'(?<!^)(?<!\. )[A-Z][a-z]+', text)))
