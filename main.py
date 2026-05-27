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


    metadata = {
        "question": question,
        "retry_count": 0,
        "chart_type": ""
    }


    result = graph.invoke(
        initial_state,
        config={
            "metadata": metadata,
            "tags": ["text2sql-agent"]
        }
    )


    if result.get("clarification_question"):

        print(
            "\nClarification:",
            result["clarification_question"]
        )

    else:

        tag = "success"


        if result.get("error_message"):

            if result.get("retry_count", 0) >= 3:
                tag = "max_retries_reached"

            else:
                tag = "self_corrected"


        elif result.get("is_empty_result"):

            tag = "empty_result"


        print(
            f"\nRun Tag: {tag}"
        )

        print(
            "\nResponse:",
            result["final_response"]
        )