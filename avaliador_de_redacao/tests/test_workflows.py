import pytest
from unittest.mock import Mock, patch
from src.workflows import calculate_final_score, setup_workflow, grade_essay
from src.config import SCORING_WEIGHTS

@pytest.fixture
def sample_state():
    """Fixture para criar um estado de exemplo com pontuações."""
    return {
        "essay": "Texto de teste",
        "relevance_score": 0.8,
        "grammar_score": 0.7,
        "structure_score": 0.9,
        "depth_score": 0.6,
        "final_score": 0.0
    }

def test_calculate_final_score(sample_state):
    """Testa o cálculo da pontuação final."""
    result = calculate_final_score(sample_state)
    
    expected_score = (
        sample_state["relevance_score"] * SCORING_WEIGHTS["relevance"] +
        sample_state["grammar_score"] * SCORING_WEIGHTS["grammar"] +
        sample_state["structure_score"] * SCORING_WEIGHTS["structure"] +
        sample_state["depth_score"] * SCORING_WEIGHTS["depth"]
    )
    
    assert result["final_score"] == expected_score

def test_setup_workflow():
    """Testa a configuração do workflow."""
    workflow = setup_workflow()
    assert workflow is not None
    # Verifica se os nós foram adicionados corretamente
    assert hasattr(workflow, "nodes")
    assert len(workflow.nodes) > 0

def test_grade_essay():
    """Testa a função principal de avaliação."""
    essay = "Texto de teste para avaliação"
    with patch('src.workflows.setup_workflow') as mock_setup:
        mock_workflow = Mock()
        mock_workflow.invoke.return_value = {
            "essay": essay,
            "relevance_score": 0.8,
            "grammar_score": 0.7,
            "structure_score": 0.9,
            "depth_score": 0.6,
            "final_score": 0.75
        }
        mock_setup.return_value = mock_workflow
        
        result = grade_essay(essay)
        
        assert result["essay"] == essay
        assert result["relevance_score"] == 0.8
        assert result["grammar_score"] == 0.7
        assert result["structure_score"] == 0.9
        assert result["depth_score"] == 0.6
        assert result["final_score"] == 0.75
        mock_workflow.invoke.assert_called_once() 