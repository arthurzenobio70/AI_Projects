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

def collection_agent(state: CustomerState) -> dict:
    """
    Gera resposta apropriada baseada na intenção do cliente e seu histórico.
    """
    context = f"""
    Dados do cliente:
    - Nome: {state['customer_name']}
    - Status do empréstimo: {state['loan_status']}
    - Dias em atraso: {state['days_overdue']}
    - Dívida total: R$ {state['total_debt']:.2f}
    - Valor da parcela atual: R$ {state['current_installment']:.2f}
    - Vencimento: {state['due_date']}
    - Intenção identificada: {state['customer_intent']}
    """
    
    prompt = PromptTemplate(
        input_variables=["context"],
        template="""Você é um agente de cobrança profissional e empático da Open Co.
        
        {context}
        
        Gere uma resposta apropriada seguindo estas diretrizes:
        1. Cumprimente o cliente pelo nome
        2. Demonstre que entendeu sua situação
        3. Ofereça uma solução clara e específica para o caso
        4. Se houver atraso, apresente opções de regularização
        5. Inclua valores e condições de forma transparente
        6. Forneça os canais de pagamento disponíveis
        7. Encerre com uma chamada para ação clara
        
        Mantenha um tom profissional, empático e objetivo."""
    )
    
    message = HumanMessage(content=prompt.format(context=context))
    response = llm.predict_messages([message]).content.strip()
    return {"agent_response": response}

def identify_customer_intent(state: CustomerState) -> dict:
    """
    Identifica a intenção do cliente baseado em sua mensagem.
    """
    intent_response = {
        "customer_intent": "",
        "intent_details": {
            "urgency_level": "",
            "payment_disposition": "",
            "negotiation_type": ""
        }
    }
    
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Analise a mensagem do cliente e identifique:

        1. Intenção principal (escolha uma):
           - RENEGOCIACAO_PARCELA
           - QUITACAO_ACORDO
           - CONSULTA_VENCIMENTO
           - CONSULTA_SALDO
           - CONTESTACAO
           - IMPOSSIBILIDADE_PAGAMENTO

        2. Nível de urgência:
           - ALTA
           - MEDIA
           - BAIXA

        3. Disposição para pagamento:
           - POSITIVA
           - NEUTRA
           - NEGATIVA

        4. Tipo de negociação desejada:
           - REDUCAO_PARCELA
           - EXTENSAO_PRAZO
           - QUITACAO
           - CARENCIA
           - NAO_APLICAVEL

        Mensagem do cliente: {text}
        
        Responda em formato JSON."""
    )
    
    message = HumanMessage(content=prompt.format(text=state["customer_intent"]))
    analysis = llm.predict_messages([message]).content.strip()
    return {"intent_analysis": analysis} 