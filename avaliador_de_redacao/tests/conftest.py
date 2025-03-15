import pytest
import os
import sys

# Adiciona o diretório raiz ao PYTHONPATH para importar os módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock das variáveis de ambiente para todos os testes."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("OPENAI_API_KEY", "test-key")
        yield 