import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


load_dotenv()


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",
    api_key=str(OPENROUTER_API_KEY),
    base_url="https://openrouter.ai/api/v1",
    temperature=0
)