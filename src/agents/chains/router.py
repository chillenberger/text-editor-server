import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.agents.prompts.router import ROUTER_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("ROUTER_MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("ROUTER_TEMPERATURE", "0"))

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

chain = ROUTER_PROMPT | llm
