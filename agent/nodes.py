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