# Text Analysis API

Esta API utiliza LangGraph e FastAPI para criar um pipeline de análise de texto que realiza três tarefas principais:
1. Classificação de texto
2. Extração de entidades
3. Sumarização

## Requisitos

- Python 3.8+
- Poetry (gerenciador de dependências)
- OpenAI API Key

## Instalação

1. Instale o Poetry (caso ainda não tenha):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone o repositório

3. Instale as dependências usando Poetry:
```bash
poetry install
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com:
```
OPENAI_API_KEY=sua_chave_api_aqui
```

## Executando a API

Para iniciar o servidor em modo de desenvolvimento:

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

A documentação interativa (Swagger UI) está disponível em:
- http://localhost:8000/docs

## Desenvolvimento

### Ambiente Virtual
Para ativar o ambiente virtual do Poetry:
```bash
poetry shell
```

### Formatação e Linting
O projeto usa várias ferramentas para garantir a qualidade do código:

- **Black** (Formatação):
```bash
poetry run black .
```

- **isort** (Ordenação de imports):
```bash
poetry run isort .
```

- **Flake8** (Linting):
```bash
poetry run flake8 .
```

- **MyPy** (Verificação de tipos):
```bash
poetry run mypy .
```

### Testes
Para executar os testes:
```bash
poetry run pytest
```

## Exemplo de Uso

```python
import requests

url = "http://localhost:8000/api/v1/analyze"
data = {
    "text": "Seu texto para análise aqui"
}

response = requests.post(url, json=data)
print(response.json())
```

## Estrutura do Projeto

```
.
├── app/
│   ├── api/
│   │   └── endpoints.py
│   ├── core/
│   │   └── config.py
│   ├── models/
│   ├── schemas/
│   │   └── text_analysis.py
│   ├── services/
│   │   └── text_analysis_service.py
│   └── main.py
├── tests/
├── .env
├── pyproject.toml
├── README.md
└── poetry.lock  # Gerado automaticamente pelo Poetry
``` 