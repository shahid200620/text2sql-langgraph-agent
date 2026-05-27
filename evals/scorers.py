def execution_accuracy(result):

    error_message = result.get(
        "error_message",
        ""
    )


    if error_message:
        return 0


    return 1



def result_accuracy(result, expected):

    final_response = result.get(
        "final_response",
        ""
    ).lower()


    expected = expected.lower()


    if expected in final_response:
        return 1


    return 0