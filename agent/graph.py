from langgraph.graph import StateGraph
from langgraph.graph import END

from agent.state import AgentState

from agent.nodes import (
    ambiguity_checker_node,
    clarification_node,
    sql_generator_node,
    sql_executor_node,
    self_correction_node,
    alternative_suggester_node,
    interpreter_node,
    chart_generator_node,
    response_composer_node,
    memory_node
)


workflow = StateGraph(AgentState)


workflow.add_node(
    "ambiguity_checker",
    ambiguity_checker_node
)

workflow.add_node(
    "clarification",
    clarification_node
)

workflow.add_node(
    "sql_generator",
    sql_generator_node
)

workflow.add_node(
    "sql_executor",
    sql_executor_node
)

workflow.add_node(
    "self_correction",
    self_correction_node
)

workflow.add_node(
    "alternative_suggester",
    alternative_suggester_node
)

workflow.add_node(
    "interpreter",
    interpreter_node
)

workflow.add_node(
    "chart_generator",
    chart_generator_node
)

workflow.add_node(
    "response_composer",
    response_composer_node
)

workflow.add_node(
    "memory",
    memory_node
)


workflow.set_entry_point(
    "ambiguity_checker"
)


def ambiguity_router(state: AgentState):

    if state["is_ambiguous"]:
        return "clarification"

    return "sql_generator"


workflow.add_conditional_edges(
    "ambiguity_checker",
    ambiguity_router
)


workflow.add_edge(
    "clarification",
    END
)


workflow.add_edge(
    "sql_generator",
    "sql_executor"
)


def execution_router(state: AgentState):

    if state["error_message"]:

        if state.get("retry_count", 0) >= 3:
            return "response_composer"

        return "self_correction"


    if state["is_empty_result"]:
        return "alternative_suggester"


    return "interpreter"


workflow.add_conditional_edges(
    "sql_executor",
    execution_router
)


workflow.add_edge(
    "self_correction",
    "sql_executor"
)


workflow.add_edge(
    "alternative_suggester",
    "response_composer"
)


workflow.add_edge(
    "interpreter",
    "chart_generator"
)

workflow.add_edge(
    "chart_generator",
    "response_composer"
)

workflow.add_edge(
    "response_composer",
    "memory"
)

workflow.add_edge(
    "memory",
    END
)


graph = workflow.compile()