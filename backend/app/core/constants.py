from enum import Enum

class Region(str, Enum):
    US = "US"
    IN = "IN"
    GLOBAL = "GLOBAL"
    UNKNOWN = "UNKNOWN"

class ConfidenceLevel(str, Enum):
    CONFIRMED = "CONFIRMED"  # Score >= 80
    PROBABLE = "PROBABLE"    # Score 50-79
    WATCH = "WATCH"          # Score < 50

class SourceType(str, Enum):
    GOVT = "GOV"      # CPSC, FDA, NHTSA, FSSAI
    NEWS = "NEWS"     # Tier-1 News
    MANUFACTURER = "MFG" # Press Releases
    OTHER = "OTHER"

# Minimum scores for confidence buckets
SCORE_CONFIRMED = 80
SCORE_PROBABLE = 50
