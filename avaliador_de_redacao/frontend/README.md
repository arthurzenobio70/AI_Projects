# Frontend - Avaliador de Redação

Este é o frontend do Avaliador de Redação, uma aplicação web construída com Streamlit que permite avaliar redações de forma interativa.

## Requisitos

- Python 3.8 ou superior
- Dependências listadas em `requirements.txt`

## Instalação

1. Instale as dependências do frontend:
```bash
pip install -r requirements.txt
```

2. Certifique-se de que todas as dependências do projeto principal também estão instaladas (na pasta raiz):
```bash
pip install -r ../requirements.txt
```

## Executando a Aplicação

Para iniciar a aplicação, execute:
```bash
streamlit run app.py
```

A aplicação estará disponível em `http://localhost:8501` por padrão.

## Funcionalidades

- Interface de chat interativa para avaliação de redações
- Avaliação em tempo real
- Histórico de avaliações
- Exibição detalhada das pontuações por critério
- Interface responsiva e amigável

## Estrutura do Projeto

```
frontend/
├── app.py              # Aplicação principal Streamlit
├── requirements.txt    # Dependências do frontend
└── README.md          # Este arquivo
```

## Integração com o Backend

O frontend se integra com o módulo de avaliação do projeto principal através do import:
```python
from src.workflows import grade_essay
```

## Contribuindo

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature
3. Faça commit das mudanças
4. Faça push para a branch
5. Abra um Pull Request 