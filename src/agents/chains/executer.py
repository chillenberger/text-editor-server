import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.agents.tools.client_tools import (
    change_file_location_tool, 
    get_workspace_structure_tool, 
    create_file_tool, 
    delete_file_tool, 
    read_file_tool,
    propose_file_change_tool
)
from src.agents.prompts.executer import EXECUTOR_PROMPT

load_dotenv()

MODEL_NAME = os.getenv("EXECUTOR_MODEL_NAME", "gpt-4o")
TEMPERATURE = float(os.getenv("EXECUTOR_TEMPERATURE", "0"))

llm = ChatOpenAI(model=MODEL_NAME, temperature=TEMPERATURE)

tools = [
    change_file_location_tool, 
    get_workspace_structure_tool, 
    create_file_tool, 
    delete_file_tool, 
    read_file_tool,
    propose_file_change_tool
]

chain = EXECUTOR_PROMPT | llm.bind_tools(tools)
