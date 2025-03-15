import os

# API Configuration
OPENAI_API_KEY = "sk-51438930b5cc469683539cd7c1c6a350"

# Model Configuration
MODEL_NAME = "deepseek-chat"
MODEL_BASE_URL = "https://api.deepseek.com"

# Scoring Weights
SCORING_WEIGHTS = {
    "relevance": 0.3,
    "grammar": 0.2,
    "structure": 0.2,
    "depth": 0.3
}

# Minimum Scores for Progression
MIN_SCORES = {
    "relevance": 0.5,
    "grammar": 0.6,
    "structure": 0.7
} 