from agent.utils import llm

from agent.state import AgentState


def ambiguity_checker_node(state: AgentState):

    question = state["question"]


    prompt = f"""
    You are an ambiguity detection system.

    Determine whether the following user question
    is ambiguous for SQL querying.

    A question is ambiguous if it is missing:
    - a country or region
    - a metric or indicator
    - a relevant time period

    Return ONLY:
    CLEAR
    or
    AMBIGUOUS

    User Question:
    {question}
    """


    response = llm.invoke(prompt)

    result = response.content.strip().upper()


    is_ambiguous = result == "AMBIGUOUS"


    return {
        "is_ambiguous": is_ambiguous,
        "clarification_needed": is_ambiguous
    }

def clarification_node(state: AgentState):

    question = state["question"]


    prompt = f"""
    You are a clarification assistant.

    The user's question is too ambiguous
    for generating a SQL query.

    Ask ONE short and focused clarification question.

    Keep it natural and concise.

    User Question:
    {question}
    """


    response = llm.invoke(prompt)

    clarification_question = response.content.strip()


    return {
        "clarification_question": clarification_question
    }

def sql_generator_node(state: AgentState):

    question = state.get(
        "clarified_question"
    ) or state["question"]


    with open(
        "prompts/sql_generator.txt",
        "r",
        encoding="utf-8"
    ) as file:

        template = file.read()


    prompt = template.format(
        question=question
    )


    response = llm.invoke(prompt)

    sql_query = response.content.strip()


    sql_query = sql_query.replace(
        "```sql",
        ""
    )

    sql_query = sql_query.replace(
        "```",
        ""
    )

    sql_query = sql_query.strip()


    sql_attempts = state.get(
        "sql_attempts",
        []
    )

    sql_attempts.append(sql_query)


    return {
        "sql_query": sql_query,
        "sql_attempts": sql_attempts
    }
import sqlite3


def sql_executor_node(state: AgentState):

    sql_query = state["sql_query"]


    try:

        conn = sqlite3.connect(
            "worldbank.db"
        )

        cursor = conn.cursor()


        cursor.execute(sql_query)


        columns = [
            description[0]
            for description in cursor.description
        ]


        rows = cursor.fetchall()


        conn.close()


        results = []

        for row in rows:

            row_data = {}

            for column, value in zip(columns, row):
                row_data[column] = value

            results.append(row_data)


        is_empty = len(results) == 0


        return {
            "execution_result": results,
            "is_empty_result": is_empty,
            "error_message": ""
        }


    except Exception as error:

        return {
            "execution_result": [],
            "is_empty_result": False,
            "error_message": str(error)
        }

