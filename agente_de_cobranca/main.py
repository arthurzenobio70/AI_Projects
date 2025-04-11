import os
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
from langsmith import Client
import langsmith
import datetime

# Load environment variables
load_dotenv()

# Set API keys
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "store_recommendation_agent"
os.environ["LANGCHAIN_TRACING_V2"] = "true"

# Initialize language model
llm = ChatOpenAI(model_name="deepseek-chat", 
    temperature=0, 
    base_url="https://api.deepseek.com/beta")

class CustomerState(TypedDict):
    """Estado do cliente e sua situação de cobrança."""
    customer_name: str
    loan_status: str
    days_overdue: int
    total_debt: float
    current_installment: float
    due_date: str
    customer_intent: str
    agent_response: str
    approved: bool
    result: str
    chat_history: List[dict]
    loan_type: str
    payment_history: List[str]
    previous_agreements: List[str]
    risk_score: str
    quitacao_disponivel: float
    processo_judicial: str

# Adicionar após as importações:
MOCK_CUSTOMER_DATABASE = {
    "123.456.789-01": {
        "customer_name": "João Silva",
        "loan_status": "atrasado",
        "days_overdue": 45,
        "total_debt": 5000.00,
        "current_installment": 250.00,
        "due_date": "2024-03-15",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2024-01-15: Atrasado", "2024-02-15: Não pago"],
        "previous_agreements": [],
        "risk_score": "alto"
    },
    "987.654.321-00": {
        "customer_name": "Maria Santos",
        "loan_status": "em_dia",
        "days_overdue": 0,
        "total_debt": 10000.00,
        "current_installment": 500.00,
        "due_date": "2024-03-20",
        "loan_type": "Crédito Consignado",
        "payment_history": ["2024-01-20: Pago", "2024-02-20: Pago"],
        "previous_agreements": [],
        "risk_score": "baixo"
    },
    "111.222.333-44": {
        "customer_name": "Pedro Oliveira",
        "loan_status": "inadimplente",
        "days_overdue": 90,
        "total_debt": 15000.00,
        "current_installment": 750.00,
        "due_date": "2023-12-10",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2023-11-10: Atrasado", "2023-12-10: Não pago", "2024-01-10: Não pago"],
        "previous_agreements": ["2023-10: Renegociação não cumprida"],
        "risk_score": "muito_alto"
    },
    "444.555.666-77": {
        "customer_name": "Ana Pereira",
        "loan_status": "renegociado",
        "days_overdue": 0,
        "total_debt": 8000.00,
        "current_installment": 300.00,
        "due_date": "2024-03-25",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2024-01-25: Pago", "2024-02-25: Pago"],
        "previous_agreements": ["2023-12: Renegociação ativa"],
        "risk_score": "médio"
    },
    "777.888.999-00": {
        "customer_name": "Carlos Ferreira",
        "loan_status": "atrasado",
        "days_overdue": 15,
        "total_debt": 3000.00,
        "current_installment": 150.00,
        "due_date": "2024-02-28",
        "loan_type": "Crédito Pessoal",
        "payment_history": ["2024-01-28: Pago", "2024-02-28: Atrasado"],
        "previous_agreements": [],
        "risk_score": "médio"
    },
    "222.333.444-55": {
        "customer_name": "Lucia Costa",
        "loan_status": "quitacao_proposta",
        "days_overdue": 60,
        "total_debt": 20000.00,
        "current_installment": 1000.00,
        "due_date": "2024-01-05",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2023-12-05: Atrasado", "2024-01-05: Não pago"],
        "previous_agreements": [],
        "risk_score": "alto",
        "quitacao_disponivel": 15000.00
    },
    "666.777.888-99": {
        "customer_name": "Roberto Almeida",
        "loan_status": "judicial",
        "days_overdue": 180,
        "total_debt": 25000.00,
        "current_installment": 1250.00,
        "due_date": "2023-09-15",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2023-08-15: Não pago", "2023-09-15: Não pago"],
        "previous_agreements": ["2023-07: Renegociação não cumprida"],
        "risk_score": "muito_alto",
        "processo_judicial": "Em andamento"
    },
    "333.444.555-66": {
        "customer_name": "Fernanda Lima",
        "loan_status": "restricao_removida",
        "days_overdue": 0,
        "total_debt": 6000.00,
        "current_installment": 300.00,
        "due_date": "2024-03-30",
        "loan_type": "Crédito Pessoal",
        "payment_history": ["2024-02-28: Regularizado"],
        "previous_agreements": ["2024-02: Acordo cumprido"],
        "risk_score": "médio"
    },
    "888.999.000-11": {
        "customer_name": "Gabriel Santos",
        "loan_status": "primeira_parcela",
        "days_overdue": 5,
        "total_debt": 2000.00,
        "current_installment": 100.00,
        "due_date": "2024-03-10",
        "loan_type": "Crédito Pessoal",
        "payment_history": [],
        "previous_agreements": [],
        "risk_score": "baixo"
    },
    "555.666.777-88": {
        "customer_name": "Patricia Souza",
        "loan_status": "ultimo_acordo",
        "days_overdue": 30,
        "total_debt": 12000.00,
        "current_installment": 600.00,
        "due_date": "2024-02-12",
        "loan_type": "Empréstimo Pessoal",
        "payment_history": ["2024-01-12: Atrasado", "2024-02-12: Não pago"],
        "previous_agreements": ["2023-11: Último acordo disponível"],
        "risk_score": "alto"
    }
}

def get_customer_info():
    """
    Busca informações do cliente na base de dados simulada.
    """
    print("\n=== Sistema de Cobrança Open Co ===")
    while True:
        print("Por favor, informe o CPF do cliente (formato: xxx.xxx.xxx-xx): ")
        cpf = input().strip()
        
        if cpf in MOCK_CUSTOMER_DATABASE:
            customer_data = MOCK_CUSTOMER_DATABASE[cpf].copy()
            customer_data["chat_history"] = []
            return customer_data
        else:
            print("\nCPF não encontrado na base de dados.")
            print("Deseja tentar novamente? (s/n): ")
            if input().strip().lower() != 's':
                return None

def interactive_chat(app, customer_state: CustomerState):
    """
    Função para manter uma conversa interativa com o cliente.
    """
    print("\n=== Iniciando atendimento ===")
    print(f"Cliente: {customer_state['customer_name']}")
    print(f"Status do empréstimo: {customer_state['loan_status']}")
    print("Digite 'sair' para encerrar o atendimento\n")

    while True:
        # Recebe input do usuário
        print("\nCliente: ", end="")
        user_input = input().strip()
        
        if user_input.lower() == 'sair':
            print("\nAtendimento encerrado. Obrigado!")
            break

        # Atualiza o estado com a nova mensagem
        current_state = customer_state.copy()
        current_state["customer_intent"] = user_input
        
        # Processa a mensagem através do workflow
        try:
            final_state = app.invoke(current_state)
            
            # Adiciona a interação ao histórico
            current_state["chat_history"].append({
                "customer": user_input,
                "agent": final_state.get("agent_response", "")
            })
            
            # Exibe a resposta do agente
            print("\nAgente: ", final_state.get("agent_response", ""))
            
            # Atualiza o estado para a próxima iteração
            customer_state = current_state
            
        except Exception as e:
            print("\nDesculpe, ocorreu um erro no processamento. Um agente humano será notificado.")
            print(f"Erro: {str(e)}")

def format_chat_history(chat_history):
    """
    Formata o histórico do chat para contextualização.
    """
    if not chat_history:
        return "Início da conversa"
    
    formatted_history = []
    for interaction in chat_history[-3:]:  # Apenas as últimas 3 interações para manter contexto relevante
        formatted_history.append(f"Cliente: {interaction['customer']}")
        if interaction.get('agent'):
            formatted_history.append(f"Agente: {interaction['agent']}")
    
    return "\n".join(formatted_history)

def identify_customer_intent(state: CustomerState) -> dict:
    """
    Identifica a intenção do cliente baseado em sua mensagem e histórico.
    """
    context = f"""
    HISTÓRICO DA CONVERSA:
    {format_chat_history(state.get('chat_history', []))}
    
    MENSAGEM ATUAL: {state['customer_intent']}
    """
    
    prompt = PromptTemplate(
        input_variables=["context"],
        template="""Você é um especialista em compreender intenções de clientes.

        {context}

        Baseado na conversa e mensagem atual, identifique a intenção principal:
        - RENEGOCIACAO_PARCELA
        - QUITACAO_ACORDO
        - CONSULTA_VENCIMENTO
        - CONSULTA_SALDO
        - CONTESTACAO
        - IMPOSSIBILIDADE_PAGAMENTO
        - ESCLARECIMENTO
        - INSATISFACAO
        
        Considere o contexto completo da conversa, não apenas a última mensagem.
        Responda APENAS com uma das opções acima."""
    )
    
    message = HumanMessage(content=prompt.format(context=context))
    intent = llm.invoke([message])
    return {"customer_intent": intent.content.strip()}

def get_negotiation_limits(state: CustomerState) -> dict:
    """
    Define os limites de negociação baseado no perfil do cliente.
    """
    base_rules = {
        "min_entrada": state['total_debt'] * 0.1,  # 10% de entrada mínima
        "max_parcelas": 12,  # máximo de parcelas padrão
        "desconto_max": 0.3,  # desconto máximo de 30%
        "carencia_maxima": 30,  # carência máxima de 30 dias
        "vencimento_min": 5,  # dia mínimo do mês
        "vencimento_max": 25,  # dia máximo do mês
    }
    
    # Ajusta regras baseado no status e histórico
    if state['loan_status'] == "judicial":
        base_rules["max_parcelas"] = 6
        base_rules["min_entrada"] = state['total_debt'] * 0.2
    elif state['risk_score'] == "muito_alto":
        base_rules["max_parcelas"] = 8
        base_rules["desconto_max"] = 0.2
    elif state['days_overdue'] > 90:
        base_rules["min_entrada"] = state['total_debt'] * 0.15
        
    return base_rules

def collection_agent(state: CustomerState) -> dict:
    """
    Gera resposta apropriada baseada na intenção do cliente e seu histórico.
    """
    # Obtém limites de negociação
    negotiation_limits = get_negotiation_limits(state)
    
    context = f"""
    CONTEXTO INTERNO (use estas informações para contextualizar sua resposta, mas não as mencione diretamente):
    - Nome: {state['customer_name']}
    - Status: {state['loan_status']}
    - Atraso: {state['days_overdue']} dias
    - Dívida: R$ {state['total_debt']:.2f}
    - Parcela: R$ {state['current_installment']:.2f}
    - Vencimento: {state['due_date']}
    - Histórico: {', '.join(state.get('payment_history', []))}
    - Acordos: {', '.join(state.get('previous_agreements', []))}
    - Risco: {state.get('risk_score', 'Não calculado')}
    
    REGRAS DE NEGOCIAÇÃO:
    - Entrada mínima: R$ {negotiation_limits['min_entrada']:.2f}
    - Máximo de parcelas: {negotiation_limits['max_parcelas']}
    - Desconto máximo: {negotiation_limits['desconto_max']*100}%
    - Carência máxima: {negotiation_limits['carencia_maxima']} dias
    - Vencimento entre dias {negotiation_limits['vencimento_min']} e {negotiation_limits['vencimento_max']}
    
    HISTÓRICO DA CONVERSA:
    {format_chat_history(state.get('chat_history', []))}
    
    INTENÇÃO ATUAL: {state['customer_intent']}
    """
    
    prompt = PromptTemplate(
        input_variables=["context"],
        template="""Você é um agente de cobrança profissional da Open Co.

        {context}

        DIRETRIZES OBRIGATÓRIAS:
        1. NUNCA aceite propostas fora dos limites estabelecidos
        2. NUNCA permita que o cliente escolha datas de vencimento além da carência máxima
        3. SEMPRE exija entrada mínima conforme as regras
        4. SEMPRE mantenha o vencimento entre os dias permitidos do mês
        5. NUNCA aceite parcelamento além do máximo permitido
        6. SEMPRE priorize acordos com entrada + parcelas
        7. NUNCA ofereça descontos além do limite estabelecido
        
        ABORDAGEM:
        1. Seja empático mas firme
        2. Apresente as condições como benefícios
        3. Direcione para soluções dentro dos parâmetros
        4. Explique gentilmente quando uma proposta está fora dos limites
        5. Sugira alternativas viáveis dentro das regras
        6. Enfatize a importância da regularização
        7. Destaque as consequências do não pagamento
        8. Mantenha o foco em soluções realistas
        
        IMPORTANTE:
        - Mantenha tom profissional e respeitoso
        - Seja direto sobre as condições disponíveis
        - Não crie falsas expectativas
        - Não permita negociações fora dos parâmetros
        - Direcione para soluções viáveis
        """
    )
    
    message = HumanMessage(content=prompt.format(context=context))
    response = llm.invoke([message])
    return {"agent_response": response.content.strip()}

def compliance_validator(state: CustomerState) -> dict:
    """
    Valida se a resposta do agente está em conformidade com as normas de cobrança.
    """
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Você é um auditor de qualidade especializado em conformidade de cobrança.
        
        Analise a resposta do agente:
        {text}
        
        Verifique se a resposta:
        1. Não contém ameaças ou coerção
        2. Mantém tom profissional e respeitoso
        3. Não divulga informações sensíveis
        4. Segue as diretrizes do Código de Defesa do Consumidor
        5. Oferece opções claras ao cliente
        
        Responda apenas com 'True' se aprovado ou 'False' se reprovado."""
    )
    
    message = HumanMessage(content=prompt.format(text=state["agent_response"]))
    validation = llm.predict_messages([message]).content.strip()
    return {"approved": validation == "True"}

def router(state: CustomerState) -> str:
    """
    Routes the workflow based on validation results.
    
    Args:
        state: Current workflow state
        
    Returns:
        Next node identifier
    """
    if state['approved']:
        return "automated_flow"
    else:
        return "human_intervention_flow"

def human_intervention_flow(state: CustomerState) -> dict:
    """
    Handles cases that require human intervention.
    
    Args:
        state: Current workflow state
        
    Returns:
        Dictionary with result message
    """
    return {'result': 'Sorry, we cannot assist you at the moment. A human agent will contact you shortly.'}

def automated_flow(state: CustomerState) -> dict:
    """
    Processa respostas aprovadas pelo validador de conformidade.
    
    Args:
        state: Estado atual do cliente e sua solicitação
        
    Returns:
        Dictionary com a resposta final aprovada
    """
    return {
        'result': (
            f"=== Resposta Aprovada ===\n"
            f"Cliente: {state['customer_name']}\n"
            f"Intenção: {state['customer_intent']}\n"
            f"Resposta: {state['agent_response']}\n"
            f"Status: Enviado automaticamente"
        )
    }

def human_intervention_flow(state: CustomerState) -> dict:
    """
    Processa casos que não foram aprovados pelo validador.
    
    Args:
        state: Estado atual do cliente e sua solicitação
        
    Returns:
        Dictionary com mensagem de necessidade de intervenção
    """
    return {
        'result': (
            f"=== Necessita Revisão Humana ===\n"
            f"Cliente: {state['customer_name']}\n"
            f"Intenção: {state['customer_intent']}\n"
            f"Resposta Sugerida: {state['agent_response']}\n"
            f"Motivo: Resposta não aprovada na validação de conformidade\n"
            f"Status: Encaminhado para supervisor"
        )
    }

def main():
    """
    Função principal para configurar e executar o workflow do agente.
    """
    # Configura o workflow
    workflow = StateGraph(CustomerState)
    
    # Adiciona nós
    workflow.add_node("identify_intent", identify_customer_intent)
    workflow.add_node("collection_agent", collection_agent)
    workflow.add_node("compliance_validator", compliance_validator)
    workflow.add_node("human_intervention_flow", human_intervention_flow)
    workflow.add_node("automated_flow", automated_flow)
    
    # Define arestas
    workflow.add_edge(START, "identify_intent")
    workflow.add_edge("identify_intent", "collection_agent")
    workflow.add_edge("collection_agent", "compliance_validator")
    workflow.add_conditional_edges(
        "compliance_validator",
        lambda x: "automated_flow" if x["approved"] else "human_intervention_flow"
    )
    workflow.add_edge("human_intervention_flow", END)
    workflow.add_edge("automated_flow", END)
    
    # Compila o grafo
    app = workflow.compile()
    
    # Inicia o loop de atendimento
    while True:
        # Obtém informações do cliente
        customer_info = get_customer_info()
        
        if customer_info is None:
            print("\nSistema finalizado.")
            break
            
        # Cria estado inicial com todas as informações do cliente
        initial_state = CustomerState(
            **customer_info,
            customer_intent="",
            agent_response="",
            approved=False,
            result=""
        )
        
        # Inicia chat interativo
        interactive_chat(app, initial_state)
        
        # Pergunta se deseja atender outro cliente
        print("\nDeseja atender outro cliente? (s/n): ")
        if input().strip().lower() != 's':
            break

    print("\nSistema finalizado.")

if __name__ == "__main__":
    main()
