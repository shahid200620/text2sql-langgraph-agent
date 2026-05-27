import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langsmith import traceable


load_dotenv()


llm = ChatOpenAI(
    model="deepseek/deepseek-chat-v3-0324",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
    temperature=0
)


@traceable(name="llm_test_call")
def test_llm():

    response = llm.invoke(
        "Say hello in one short sentence."
    )

    return response.content