from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel
from typing import Type
import os

MODEL_NAME = os.getenv("LLM_MODEL", "gpt-4o-mini")

def get_llm():
    return ChatOpenAI(
        model=MODEL_NAME,
        temperature=0,
        max_retries=3,
    )

def get_structured_llm(output_schema: Type[BaseModel]):
    return get_llm().with_structured_output(output_schema)