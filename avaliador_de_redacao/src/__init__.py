"""
Avaliador de Redação - Um sistema de avaliação de redações usando LangGraph e LLMs.
"""

from .workflows import grade_essay
from .agents import EssayEvaluator

__all__ = ['grade_essay', 'EssayEvaluator'] 