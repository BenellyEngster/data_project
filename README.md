# Coletor Web Automatizado & Pipeline de Dados (`data_project`)

Um projeto de coleta automatizada de dados e arquitetura de pipeline construído com **Python**, **Selenium WebDriver** e **Pandas**.

Este projeto foi desenvolvido para conectar a extração automatizada de dados da web (*web scraping*) com a análise de dados, servindo como base para pesquisas acadêmicas e projetos de Ciência de Dados.

---

## Arquitetura do Projeto

Para manter o código limpo e com separação clara de responsabilidades, o repositório está estruturado de forma modular:

```text
data_project/
├── .venv/                   # Ambiente Virtual isolado do Python
├── data/
│   └── homicidios-e-feminicidios.csv  # Base de dados de exemplo para validação de estrutura
├── main.py                  # Script principal de execução (Orquestrador)
├── scraper.py               # Lógica de raspagem web e automação do navegador (Selenium)
├── treatment.py             # Lógica de limpeza e transformação dos dados (Pandas)
├── database.py              # Lógica de conexão e salvamento em banco de dados
└── README.md                # Documentação do projeto
