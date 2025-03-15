import os

# API Configuration

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
