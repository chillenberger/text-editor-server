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
    new_message: Message
    mode: str = "execute" # "plan" or "execute" or "auto"
    special_instructions: str | None = None

@chain
async def general_agent(req: dict):
    print("\n/Request Mode/")
    
    try:
        if isinstance(req, dict):
            req = Request(**req)

        print("\n/New Message/")
        print(req.new_message)
        print(req.mode)
        print(req.special_instructions)

        # 1. Reconstruct History
        input_messages = []
        for msg in (req.messages + [req.new_message]):
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
        print("Special Instructions:")
        print(special_instructions)

        # 2. Determine Mode
        mode = req.mode
        if mode == "auto":
            print("Routing Request...")
            router_response = await router_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})
            mode = router_response.content.strip().lower()
            print(f"Router decided: {mode}")

        # 3. Plan Mode
        if "execute" not in mode: # execute not in makes more likely to execute
            print(f"Planning...")
            response = await planner_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})
            # Planner just talks
            print("\n/Planner Response/")
            print(response.content)
            return {
                "message": {
                    "type": "assistant",
                    "content": response.content,
                },
                "mode": "planned"
            }
        
        else: # Default to execute
            print(f"Executing Step...")
            response = await executor_chain.ainvoke({"messages": input_messages, "special_instructions": special_instructions})

            print("\n/Executor Response/")
            print(response.content)
            
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
