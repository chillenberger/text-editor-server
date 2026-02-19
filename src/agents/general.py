import traceback
from langchain_core.messages import (
    HumanMessage,
    ToolMessage,
    AIMessage,
)
from langchain_core.runnables import chain
from pydantic import BaseModel
from dotenv import load_dotenv

from src.chains.router import chain as router_chain
from src.chains.executer import chain as executor_chain
from src.chains.planner import chain as planner_chain
from src.prompts.base import get_reference_files_prompt

load_dotenv()

# Request Models
class Message(BaseModel):
    type: str
    content: str | None = None
    tool_call_id: str | None = None
    tool_name: str | None = None
    tool: dict | None = None

class Request(BaseModel):
    messages: list[Message]
    mode: str = "execute" # "plan" or "execute" or "auto"
    special_instructions: str | None = None
    reference_files: list[str] | None = None

@chain
async def general_agent(req: dict):
    try:
        if isinstance(req, dict):
            req = Request(**req)

        # 1. Reconstruct History
        input_messages = []
        for msg in req.messages:
            match msg.type:
                case "human":
                    input_messages.append(HumanMessage(content=msg.content or ""))
                case "assistant":
                    input_messages.append(AIMessage(content=msg.content or ""))
                case "tool":
                    input_messages.append(ToolMessage(
                        content=msg.content or "", 
                        tool_call_id=msg.tool_call_id or "unknown", 
                        tool_name=msg.tool_name or "unknown"
                    ))
                case "tool_call":
                    input_messages.append(AIMessage(content="", tool_calls=[msg.tool]))

        special_instructions = req.special_instructions or "No user constraints provided."

        # 1.5. Add Reference Files
        input_messages[-1].content = f"{input_messages[-1].content}\n{get_reference_files_prompt(req.reference_files)}"
        
        # 2. Determine Mode
        mode = req.mode
        if mode == "auto":
            router_response = await router_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})
            mode = router_response.content.strip().lower()

        # 3. Plan Mode
        if "execute" not in mode:
            response = await planner_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})
            return {
                "message": {
                    "type": "assistant",
                    "content": response.content,
                },
                "mode": "planned"
            }
        
        else: # Default to execute
            response = await executor_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})
            
            # Execute Step Logic
            if response.tool_calls:
                return {
                    "message": {
                        "type": "tool_call",
                        "tool": response.tool_calls[0],
                    },
                    "mode": "executed"
                }
            else:
                return {
                    "message": {
                        "type": "assistant",
                        "content": response.content,
                    },
                    "mode": "executed"
                }

    except Exception as e:
        print(f"Error in plan: {e}")
        traceback.print_exc()
        return {
            "message": {
                "type": "assistant",
                "content": f"I encountered an error while processing your request: {str(e)}. Please try again."
            },
            "mode": "executed"
        }
