from app.core.constants import SourceType, ConfidenceLevel, SCORE_CONFIRMED, SCORE_PROBABLE

class ConfidenceScorer:
    # 6.1 Scoring Model
    POINTS_MAP = {
        SourceType.GOVT: 50,
        SourceType.MANUFACTURER: 40,
        SourceType.NEWS: 25,
        "multiple_confirmations": 20,
        "model_batch_specified": 15,
        "india_mentioned": 30
    }

    @classmethod
    def calculate_score(cls, source_type: SourceType, nlp_analysis: dict) -> int:
        score = 0
        
        # Base Points by Source
        score += cls.POINTS_MAP.get(source_type, 0)
        
        # NLP Bonuses
        if nlp_analysis.get("is_india", False):
            score += cls.POINTS_MAP["india_mentioned"]
            
        # Check for model/batch info (basic heuristic from NLP extraction)
        # Using a simple check if any entities were extracted for now
        # Phase 4 advanced: Check specifically for "Model X" or "Batch Y" patterns
        entities = nlp_analysis.get("entities", [])
        if entities: 
             score += cls.POINTS_MAP["model_batch_specified"]

        # TODO: "Multiple confirmations" requires checking DB for duplicates (Phase 4 extension)
        
        return score

    @classmethod
    def get_bucket(cls, score: int) -> ConfidenceLevel:
        if score >= SCORE_CONFIRMED:
            return ConfidenceLevel.CONFIRMED
        elif score >= SCORE_PROBABLE:
            return ConfidenceLevel.PROBABLE
        else:
            return ConfidenceLevel.WATCH
