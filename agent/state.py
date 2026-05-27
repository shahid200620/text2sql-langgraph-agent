from typing import TypedDict, List, Dict, Any


class AgentState(TypedDict):

    question: str

    clarified_question: str

    is_ambiguous: bool

    clarification_needed: bool

    clarification_question: str

    sql_query: str

    sql_attempts: List[str]

    retry_count: int

    execution_result: List[Dict[str, Any]]

    is_empty_result: bool

    error_message: str

    interpretation: str

    chart_spec: Dict[str, Any]

    final_response: str

    messages: List[Dict[str, str]]

    follow_up_context: Dict[str, Any]