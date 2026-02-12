from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.prompts.base import get_system_prompt

ROUTER_CORE_PROMPT = """You are an intelligent router.
Your job is to decide if the user's request requires a formal step-by-step PLAN or if it can be EXECUTED directly.

- **PLAN**: Use this for complex tasks or high-level questions that you don't believe can be executed directly by a modern AI assistant. Do not do this if unsure.
- **EXECUTE**: Use this for simple questions or questions you believe can be executed directly by a modern AI assistant. If unsure default to this.

Output ONLY the word 'PLAN' or 'EXECUTE'.
"""

ROUTER_SYSTEM_PROMPT = get_system_prompt(ROUTER_CORE_PROMPT)

ROUTER_PROMPT = ChatPromptTemplate.from_messages([
    ("system", ROUTER_SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="messages"),
])
