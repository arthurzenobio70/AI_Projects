import re
from typing import Dict, Any

def extract_score(content: str) -> float:
    """
    Extrai a pontuação numérica do texto da resposta.
    Formato esperado no texto: 'Pontuação: 0.75'.
    """
    match = re.search(r'Pontuação:\s*(\d+(\.\d+)?)', content)
    if match:
        return float(match.group(1))
    raise ValueError(f"Não foi possível extrair a pontuação de: {content}")

def create_initial_state(essay: str) -> Dict[str, Any]:
    """
    Cria o estado inicial para o workflow de avaliação.
    """
    return {
        "essay": essay,
        "relevance_score": 0.0,
        "grammar_score": 0.0,
        "structure_score": 0.0,
        "depth_score": 0.0,
        "final_score": 0.0
    } 