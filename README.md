# Text-to-SQL LangGraph Agent

A conversational AI agent built using LangChain and LangGraph that converts natural language questions into SQLite queries for World Bank development data.

---

# Features

- Natural Language → SQL generation
- LangGraph state machine workflow
- SQL execution with retry correction
- Ambiguity detection and clarification
- Conversational memory
- Chart specification generation
- Empty-result handling
- Evaluation dataset and scorers
- LangSmith-ready prompt architecture

---

# Project Structure

```txt
agent/
setup/
prompts/
evals/
main.py
worldbank.db
requirements.txt
Dockerfile
docker-compose.yml
README.md
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone https://github.com/shahid200620/text2sql-langgraph-agent.git
cd text2sql-langgraph-agent
```

---

## 2. Create Virtual Environment

### Windows CMD

```cmd
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```cmd
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create `.env` file using `.env.example`

Example:

```env
OPENROUTER_API_KEY=your_api_key
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=text2sql-agent
```

---

## 5. Load Database

```cmd
python setup\load_data.py
```

---

## 6. Verify Database

```cmd
python setup\verify_db.py
```

---

## 7. Run Application

```cmd
python main.py
```

---

# Example Questions

- What was Germany GDP growth in 2022?
- Top 5 countries by population
- GDP trend in China
- Compare GDP between Germany and France
- Health spending correlation with life expectancy

---

# Docker Usage

## Build Container

```bash
docker compose build
```

## Run Application

```bash
docker compose up
```

---

# Evaluation

Evaluation dataset:

```txt
evals/dataset.json
```

Scorers:

```txt
evals/scorers.py
```

---

# Technologies Used

- Python
- LangChain
- LangGraph
- SQLite
- Pandas
- OpenRouter
- LangSmith

---

# Author

Shahid Mohammed
