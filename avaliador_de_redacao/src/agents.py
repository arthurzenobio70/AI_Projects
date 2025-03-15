from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from .config import OPENAI_API_KEY, MODEL_NAME, MODEL_BASE_URL
from .utils import extract_score

# Initialize LLM
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model=MODEL_NAME,
    base_url=MODEL_BASE_URL
)

class EssayEvaluator:
    """Classe que implementa os agentes de avaliação de redação."""
    
    @staticmethod
    def check_relevance(state: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica a relevância da redação."""
        prompt = ChatPromptTemplate.from_template(
            "Analise a relevância da seguinte redação com base no tema. "
            "Forneça uma pontuação de 0 a 1, iniciando sua resposta com 'Pontuação: '.\n\nRedação: {essay}"
        )
        result = llm.invoke(prompt.format(essay=state["essay"]))
        state["relevance_score"] = extract_score(result.content)
        return state

    @staticmethod
    def check_grammar(state: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica a gramática da redação."""
        prompt = ChatPromptTemplate.from_template(
            "Avalie a gramática do texto. Forneça uma pontuação de 0 a 1 iniciando com 'Pontuação: '.\n\nRedação: {essay}"
        )
        result = llm.invoke(prompt.format(essay=state["essay"]))
        state["grammar_score"] = extract_score(result.content)
        return state

    @staticmethod
    def analyze_structure(state: Dict[str, Any]) -> Dict[str, Any]:
        """Verifica a estrutura textual da redação."""
        prompt = ChatPromptTemplate.from_template(
            "Avalie a estrutura do texto e forneça uma pontuação de 0 a 1 iniciando com 'Pontuação: '.\n\nRedação: {essay}"
        )
        result = llm.invoke(prompt.format(essay=state["essay"]))
        state["structure_score"] = extract_score(result.content)
        return state

    @staticmethod
    def evaluate_depth(state: Dict[str, Any]) -> Dict[str, Any]:
        """Avalia a profundidade da análise nos argumentos da redação."""
        prompt = ChatPromptTemplate.from_template(
            "Avalie a profundidade da argumentação no texto. Forneça uma pontuação de 0 a 1 iniciando com 'Pontuação: '.\n\nRedação: {essay}"
        )
        result = llm.invoke(prompt.format(essay=state["essay"]))
        state["depth_score"] = extract_score(result.content)
        return state 