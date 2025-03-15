import pytest
from src.utils import extract_score, create_initial_state

def test_extract_score_valid():
    """Testa a extração de pontuação de um texto válido."""
    content = "Pontuação: 0.75"
    assert extract_score(content) == 0.75

def test_extract_score_invalid():
    """Testa a extração de pontuação de um texto inválido."""
    content = "Texto sem pontuação"
    with pytest.raises(ValueError):
        extract_score(content)

def test_create_initial_state():
    """Testa a criação do estado inicial."""
    essay = "Texto de teste"
    state = create_initial_state(essay)
    
    assert state["essay"] == essay
    assert state["relevance_score"] == 0.0
    assert state["grammar_score"] == 0.0
    assert state["structure_score"] == 0.0
    assert state["depth_score"] == 0.0
    assert state["final_score"] == 0.0 