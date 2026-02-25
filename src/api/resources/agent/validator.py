from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

# Request Models
class Message(BaseModel):
    type: str
    content: str | None = None
    tool_call_id: str | None = None
    tool_name: str | None = None
    tool: dict | None = None

class AgentRequest(BaseModel):
    messages: list[Message]
    mode: str = "execute"
    special_instructions: str | None = None
    reference_files: list[str] | None = None

class AgentOutputs(BaseModel):
    message: Message
    mode: str = "execute"

# Parse the request to Langchain format, use hints for langchain typing
def parse_request_to_langchain(req: dict) -> dict:
    req = AgentRequest(**req)

    messages: list[Message] = []
    for msg in req.messages:
        if msg.type == "human":
            messages.append(HumanMessage(content=msg.content or ""))
        elif msg.type == "assistant":
            messages.append(AIMessage(content=msg.content or ""))
        elif msg.type == "tool":
            messages.append(ToolMessage(
                content=msg.content or "", 
                tool_call_id=msg.tool_call_id or "unknown", 
                name=msg.tool_name or "unknown"
            ))
        elif msg.type == "tool_call":
            messages.append(AIMessage(content="", tool_calls=[msg.tool]))
    
    return {
        "messages": messages,
        "mode": req.mode,
        "special_instructions": req.special_instructions or "No user constraints provided.",
        "reference_files": req.reference_files,
    }

parse_and_validate = RunnableLambda(parse_request_to_langchain).with_types(input_type=dict, output_type=dict)