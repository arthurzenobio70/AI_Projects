import pytest
from unittest.mock import Mock, patch
from src.agents import EssayEvaluator

@pytest.fixture
def mock_llm():
    """Fixture para mockar o LLM."""
    with patch('src.agents.llm') as mock:
        mock.invoke.return_value = Mock(content="Pontuação: 0.8")
        yield mock

@pytest.fixture
def sample_state():
    """Fixture para criar um estado de exemplo."""
    return {
        "essay": "Texto de teste para avaliação",
        "relevance_score": 0.0,
        "grammar_score": 0.0,
        "structure_score": 0.0,
        "depth_score": 0.0,
        "final_score": 0.0
    }

def test_check_relevance(mock_llm, sample_state):
    """Testa a avaliação de relevância."""
    result = EssayEvaluator.check_relevance(sample_state)
    assert result["relevance_score"] == 0.8
    mock_llm.invoke.assert_called_once()

def test_check_grammar(mock_llm, sample_state):
    """Testa a avaliação de gramática."""
    result = EssayEvaluator.check_grammar(sample_state)
    assert result["grammar_score"] == 0.8
    mock_llm.invoke.assert_called_once()

def test_analyze_structure(mock_llm, sample_state):
    """Testa a análise de estrutura."""
    result = EssayEvaluator.analyze_structure(sample_state)
    assert result["structure_score"] == 0.8
    mock_llm.invoke.assert_called_once()

def test_evaluate_depth(mock_llm, sample_state):
    """Testa a avaliação de profundidade."""
    result = EssayEvaluator.evaluate_depth(sample_state)
    assert result["depth_score"] == 0.8
    mock_llm.invoke.assert_called_once() 