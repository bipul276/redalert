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
    INDIA_HIGH_SCORE_KEYWORDS = {
        "fssai", "cdsco", "drug controller", "state fda"
    }
    
    INDIA_LOW_SCORE_KEYWORDS = {
        "india", "indian", "delhi", "mumbai", "bangalore", "telangana", 
        "bis", "morth", "dgca", "rupee", "rs."
    }
    
    FOREIGN_HIGH_SCORE_KEYWORDS = {
        "swissmedic", "fda", "mhra", "hsa", "tga", "cpsc", "cfia"
    }

    FOREIGN_LOW_SCORE_KEYWORDS = {
        "usa", "u.s.", "united states", "canada", "ontario", "toronto", "vancouver", "montreal",
        "nigeria", "africa", "japan", "australia", "sydney", "melbourne", "brisbane",
        "uk", "united kingdom", "london", "dublin", "ireland", "new zealand", "europe", "eu",
        "california", "texas", "ohio", "new york",
        "russia", "ukraine", "swiss", "switzerland", "china"
    }

    # 5.4 Stage 4: Food & Medicine Context (Strict Filtering)
    FOOD_MED_KEYWORDS = {
        "food", "drink", "beverage", "snack", "spice", "dairy", "meat", 
        "candy", "chocolate", "grocery", "restaurant", "fssai", "dietary",
        "supplement", "medicine", "drug", "pharma", "pharmacy", "pill", 
        "tablet", "syrup", "cdsco", "fda", "eating", "consumption", "poisoning",
        "adulteration", "adulterated", "sweet", "milk", "ghee", "khoya",
        "paneer", "oil", "water", "juice", "bakery", "masala"
    }

    @classmethod
    def analyze_text(cls, text: str) -> Dict[str, Any]:
        text_lower = text.lower()
        
        # 1. Intent Detection
        intent_score = 0
        found_keywords = []
        for kw in cls.RECALL_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                intent_score += 1
                found_keywords.append(kw)
        
        is_recall = intent_score > 0 # Hard gate: must have at least one keyword

        # 2. Region Scoring (Replaces simple booleans)
        india_score = 0
        for kw in cls.INDIA_HIGH_SCORE_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                india_score += 5
        
        for kw in cls.INDIA_LOW_SCORE_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                india_score += 2
                
        foreign_score = 0
        for kw in cls.FOREIGN_HIGH_SCORE_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                foreign_score += 5
                
        for kw in cls.FOREIGN_LOW_SCORE_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                foreign_score += 2

        is_india = india_score >= 5 and india_score >= (foreign_score + 2)

        # 3. Food/Medicine Context Detection
        food_med_score = 0
        for kw in cls.FOOD_MED_KEYWORDS:
            if re.search(rf'\b{re.escape(kw)}\b', text_lower):
                food_med_score += 1
                
        is_food_med = food_med_score > 0

        return {
            "is_recall": is_recall,
            "intent_score": intent_score,
            "intent_keywords": found_keywords,
            "is_india": is_india,
            "india_score": india_score,
            "foreign_score": foreign_score,
            "is_food_med": is_food_med,
            "food_med_score": food_med_score
        }

    @classmethod
    def extract_entity_candidates(cls, text: str):
        # Very basic regex for capitalized words (potential brands) - Stage 2 (Lite)
        # In a real app, this would be spaCy.
        # Captures "Brand Name" distinct from start of sentences
        return list(set(re.findall(r'(?<!^)(?<!\. )[A-Z][a-z]+', text)))
