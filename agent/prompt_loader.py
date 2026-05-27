def load_prompt(prompt_name):

    prompt_paths = {
        "text-to-sql-generator":
        "prompts/sql_generator.txt",

        "result-interpreter":
        "prompts/interpreter.txt",

        "ambiguity-checker":
        "prompts/ambiguity_checker.txt",

        "clarification-asker":
        "prompts/clarification_asker.txt"
    }


    path = prompt_paths.get(prompt_name)


    if not path:
        raise ValueError(
            f"Prompt not found: {prompt_name}"
        )


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()