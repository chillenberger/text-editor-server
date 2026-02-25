from src.api.resources.agent.validator import parse_request_to_langchain
from src.agents.orchestrator import agent_controller

chain = parse_request_to_langchain | agent_controller