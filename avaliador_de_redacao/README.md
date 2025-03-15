# 📝 Avaliador de Redação com IA

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-1.7.0+-pink.svg)](https://python-poetry.org/)

## 📑 Índice 

* [Sobre o Projeto](#-sobre-o-projeto)
* [Status do Projeto](#-status-do-projeto)
* [Estrutura do Projeto](#-estrutura-do-projeto)
* [Como Executar](#-como-executar)
* [Tecnologias](#-tecnologias)
* [Próximos Passos](#-próximos-passos)
* [Contribuindo](#-contribuindo)
* [Licença](#-licença)

## 💡 Sobre o Projeto

O Avaliador de Redação com IA é uma ferramenta em desenvolvimento que visa automatizar o processo de avaliação de redações utilizando modelos de linguagem natural (LLMs). O projeto está em seus estágios iniciais, focando na estruturação da arquitetura base e implementação das funcionalidades principais.

### Funcionalidades Atuais
- ✅ Estrutura base do projeto
- ✅ Configuração inicial dos agentes de IA
- ✅ Esqueleto da interface web
- ✅ Integração com LLMs
- ✅ Sistema de avaliação básico
- ✅ Interface web funcional

## 📁 Estrutura do Projeto

```
avaliador_de_redacao/
├── src/                    # Código fonte principal
│   ├── agents.py          # Implementação dos agentes de IA
│   ├── workflows.py       # Fluxos de trabalho e lógica principal
│   ├── utils.py           # Utilitários e funções auxiliares
│   └── config.py          # Configurações do sistema
├── frontend/              # Interface web
│   ├── app.py            # Aplicação Streamlit
│   └── requirements.txt   # Dependências do frontend
├── tests/                 # Testes unitários
│   ├── test_agents.py
│   ├── test_utils.py
│   └── test_workflows.py
├── .gitignore             # Arquivos e pastas ignorados pelo Git
├── LICENSE                # Licença do projeto
├── pyproject.toml         # Configurações do Poetry
├── README.md              # Documentação do projeto
├── requirements.txt       # Dependências principais
├── setup.py               # Script de instalação do projeto
```

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- Poetry

### Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/avaliador_de_redacao.git
cd avaliador_de_redacao

# Instale as dependências com Poetry
poetry install

# Ative o ambiente virtual
poetry shell

# Execute a aplicação
poetry run python main.py
```

## 🛠️ Tecnologias

### Core
- [Python](https://www.python.org/) - Linguagem principal
- [LangChain](https://langchain.com/) - Framework para LLMs
- [OpenAI GPT](https://openai.com/) - Modelo de linguagem

### Frontend
- [Streamlit](https://streamlit.io/) - Interface web

### Desenvolvimento
- [Poetry](https://python-poetry.org/) - Gerenciamento de dependências
- [pytest](https://pytest.org/) - Framework de testes

## 📈 Próximos Passos

1. Implementação da Integração com LLMs
   - Configuração dos modelos de linguagem
   - Desenvolvimento dos prompts de avaliação
   - Testes de acurácia

2. Desenvolvimento da Interface
   - Criação do frontend básico
   - Implementação do upload de redações
   - Sistema de visualização de resultados

3. Sistema de Avaliação
   - Implementação dos critérios de avaliação
   - Desenvolvimento do sistema de pontuação
   - Geração de feedback estruturado

## 🤝 Contribuindo

Para contribuir com o projeto:
1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`)
3. Faça commit das mudanças (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nome-da-feature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">Projeto em desenvolvimento inicial - Contribuições são bem-vindas!</p>
