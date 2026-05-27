from agent.graph import graph


while True:

    question = input("\nAsk a question: ")


    if question.lower() == "exit":
        break


    initial_state = {
        "question": question,
        "clarified_question": "",
        "is_ambiguous": False,
        "clarification_needed": False,
        "clarification_question": "",
        "sql_query": "",
        "sql_attempts": [],
        "retry_count": 0,
        "execution_result": [],
        "is_empty_result": False,
        "error_message": "",
        "interpretation": "",
        "chart_spec": {},
        "final_response": "",
        "messages": [],
        "follow_up_context": {}
    }


    result = graph.invoke(initial_state)


    if result.get("clarification_question"):

        print(
            "\nClarification:",
            result["clarification_question"]
        )

    else:

        print(
            "\nResponse:",
            result["final_response"]
        )