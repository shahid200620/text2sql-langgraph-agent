from agent.prompt_loader import load_prompt

from agent.utils import llm

from agent.state import AgentState


def ambiguity_checker_node(state: AgentState):

    question = state["question"].lower()


    countries = [
        "germany",
        "france",
        "india",
        "china",
        "japan",
        "brazil",
        "canada",
        "united states"
    ]


    metrics = [
        "gdp",
        "gdp growth",
        "population",
        "health",
        "life expectancy",
        "unemployment",
        "growth"
    ]


    has_country = any(
        country in question
        for country in countries
    )


    has_metric = any(
        metric in question
        for metric in metrics
    )


    has_year = any(
        word.replace("?", "").isdigit()
        and len(word.replace("?", "")) == 4
        for word in question.split()
    )


    is_ambiguous = (
        not has_country
        or not has_metric
        or not has_year
    )


    vague_questions = [
        "how is the economy doing",
        "tell me about development",
        "show economic performance"
    ]


    if any(
        vague in question
        for vague in vague_questions
    ):
        is_ambiguous = True


    return {
        "is_ambiguous": is_ambiguous,
        "clarification_needed": is_ambiguous
    }


def clarification_node(state: AgentState):

    question = state["question"]


    prompt = f"""
    Ask one short clarification question.

    Do not explain anything.
    Do not add introductions.
    Do not use markdown.

    Keep it under 20 words.

    User Question:
    {question}
    """


    response = llm.invoke(prompt)

    clarification_question = response.content.strip()


    clarification_question = (
        clarification_question
        .replace("*", "")
        .replace('"', "")
    )


    return {
        "clarification_question": clarification_question
    }

def sql_generator_node(state: AgentState):

    question = state.get(
        "clarified_question"
    ) or state["question"]


    template = load_prompt(
        "text-to-sql-generator"
    )


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

def self_correction_node(state: AgentState):

    question = state["question"]

    failed_query = state["sql_query"]

    error_message = state["error_message"]

    retry_count = state.get(
        "retry_count",
        0
    )


    prompt = f"""
    You are a SQLite query correction system.

    The previous SQL query failed.

    Fix the query using the database schema
    and the error message.

    Return ONLY corrected SQL.

    DATABASE SCHEMA

    Table: indicators

    Columns:
    - country
    - date
    - gdp_current_usd
    - gdp_per_capita_usd
    - gdp_growth_pct
    - population
    - health_expenditure_pct_gdp
    - life_expectancy
    - co2_emissions_per_capita
    - unemployment_pct

    Table: country_metadata

    Columns:
    - country_code
    - country_name
    - region
    - income_group
    - lending_type

    RULES:
    - Never use SELECT *
    - Always use LIMIT 20
    - Return ONLY SQL
    - No markdown

    USER QUESTION:
    {question}

    FAILED SQL:
    {failed_query}

    ERROR:
    {error_message}
    """


    response = llm.invoke(prompt)

    corrected_sql = response.content.strip()


    corrected_sql = corrected_sql.replace(
        "```sql",
        ""
    )

    corrected_sql = corrected_sql.replace(
        "```",
        ""
    )

    corrected_sql = corrected_sql.strip()


    sql_attempts = state.get(
        "sql_attempts",
        []
    )

    sql_attempts.append(corrected_sql)


    return {
        "sql_query": corrected_sql,
        "sql_attempts": sql_attempts,
        "retry_count": retry_count + 1
    }

def alternative_suggester_node(state: AgentState):

    question = state["question"]


    prompt = f"""
    You are a helpful data assistant.

    The SQL query returned no results.

    Suggest a useful alternative.

    Possible suggestions:
    - nearest available year
    - checking another country
    - trying a broader query

    Keep the response short and natural.

    User Question:
    {question}
    """


    response = llm.invoke(prompt)

    suggestion = response.content.strip()


    return {
        "interpretation": suggestion
    }

def interpreter_node(state: AgentState):

    question = state["question"]

    result = state["execution_result"]


    template = load_prompt(
        "result-interpreter"
    )


    prompt = template.format(
        question=question,
        result=result
    )


    response = llm.invoke(prompt)

    interpretation = response.content.strip()


    return {
        "interpretation": interpretation
    }

def chart_generator_node(state: AgentState):

    question = state["question"].lower()

    results = state["execution_result"]


    if "over time" in question or "trend" in question:

        chart_spec = {
            "chart_type": "line",
            "x_axis": "date",
            "y_axis": "value",
            "title": "Trend Over Time"
        }


    elif "correlation" in question or "relationship" in question:

        chart_spec = {
            "chart_type": "scatter",
            "x_axis": "x",
            "y_axis": "y",
            "title": "Correlation Analysis"
        }


    elif "top" in question or "compare" in question:

        chart_spec = {
            "chart_type": "bar",
            "x_axis": "country",
            "y_axis": "value",
            "title": "Comparison Chart"
        }


    else:

        prompt = f"""
        You are a chart recommendation assistant.

        Based on the user question and SQL results,
        generate a chart specification.

        Return ONLY a Python dictionary.

        Allowed chart types:
        - bar
        - line
        - scatter
        - pie

        Include:
        - chart_type
        - x_axis
        - y_axis
        - title

        User Question:
        {question}

        SQL Results:
        {results}
        """


        response = llm.invoke(prompt)

        content = response.content.strip()


        try:

            chart_spec = eval(content)

        except Exception:

            chart_spec = {
                "chart_type": "bar",
                "x_axis": "country",
                "y_axis": "value",
                "title": "Data Visualization"
            }


    return {
        "chart_spec": chart_spec
    }

def response_composer_node(state: AgentState):

    interpretation = state.get(
        "interpretation",
        ""
    )

    chart_spec = state.get(
        "chart_spec",
        {}
    )


    response = interpretation


    if chart_spec:

        chart_type = chart_spec.get(
            "chart_type",
            "chart"
        )

        title = chart_spec.get(
            "title",
            "Data Visualization"
        )


        response += (
            f"\n\nSuggested Visualization: "
            f"{chart_type.title()} Chart"
            f" - {title}"
        )


    return {
        "final_response": response
    }

def memory_node(state: AgentState):

    question = state["question"]


    context = state.get(
        "follow_up_context",
        {}
    )


    countries = [
        "Germany",
        "France",
        "India",
        "China",
        "United States",
        "Japan",
        "Brazil",
        "Canada"
    ]


    metrics = {
        "gdp": "gdp_current_usd",
        "growth": "gdp_growth_pct",
        "population": "population",
        "life expectancy": "life_expectancy",
        "unemployment": "unemployment_pct",
        "health": "health_expenditure_pct_gdp"
    }


    for country in countries:

        if country.lower() in question.lower():

            context["country"] = country


    for keyword, metric in metrics.items():

        if keyword in question.lower():

            context["metric"] = metric


    words = question.split()

    for word in words:

        cleaned_word = word.replace("?", "").replace(",", "")

        if cleaned_word.isdigit() and len(cleaned_word) == 4:

            context["year"] = cleaned_word


    return {
        "follow_up_context": context
    }


