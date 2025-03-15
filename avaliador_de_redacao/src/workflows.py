from typing import Dict, Any
from langgraph.graph import StateGraph, END
from .agents import EssayEvaluator
from .config import SCORING_WEIGHTS, MIN_SCORES
from .utils import create_initial_state

class State(dict):
    """Definição dos atributos do estado no fluxo de trabalho."""
    essay: str
    relevance_score: float
    grammar_score: float
    structure_score: float
    depth_score: float
    final_score: float

def calculate_final_score(state: Dict[str, Any]) -> Dict[str, Any]:
    """Calcula a pontuação final ponderada da redação."""
    state["final_score"] = (
        state["relevance_score"] * SCORING_WEIGHTS["relevance"] +
        state["grammar_score"] * SCORING_WEIGHTS["grammar"] +
        state["structure_score"] * SCORING_WEIGHTS["structure"] +
        state["depth_score"] * SCORING_WEIGHTS["depth"]
    )
    return state

def setup_workflow() -> StateGraph:
    """Configura e retorna o workflow de avaliação."""
    workflow = StateGraph(State)
    
    # Adiciona os nós do grafo
    workflow.add_node("check_relevance", EssayEvaluator.check_relevance)
    workflow.add_node("check_grammar", EssayEvaluator.check_grammar)
    workflow.add_node("analyze_structure", EssayEvaluator.analyze_structure)
    workflow.add_node("evaluate_depth", EssayEvaluator.evaluate_depth)
    workflow.add_node("calculate_final_score", calculate_final_score)

    # Adiciona as arestas condicionais
    workflow.add_conditional_edges(
        "check_relevance",
        lambda x: "check_grammar" if x["relevance_score"] > MIN_SCORES["relevance"] else "calculate_final_score"
    )
    workflow.add_conditional_edges(
        "check_grammar",
        lambda x: "analyze_structure" if x["grammar_score"] > MIN_SCORES["grammar"] else "calculate_final_score"
    )
    workflow.add_conditional_edges(
        "analyze_structure",
        lambda x: "evaluate_depth" if x["structure_score"] > MIN_SCORES["structure"] else "calculate_final_score"
    )
    workflow.add_conditional_edges("evaluate_depth", lambda x: "calculate_final_score")

    # Configura o ponto de entrada e saída
    workflow.set_entry_point("check_relevance")
    workflow.add_edge("calculate_final_score", END)

    return workflow.compile()

def grade_essay(essay: str) -> Dict[str, Any]:
    """Executa o workflow de avaliação da redação."""
    workflow = setup_workflow()
    initial_state = create_initial_state(essay)
    return workflow.invoke(initial_state) 