import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.prompts.planner import PLANNER_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("PLANNER_MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("PLANNER_TEMPERATURE", "0"))

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

chain = PLANNER_PROMPT | llm