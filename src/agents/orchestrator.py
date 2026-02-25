import traceback
from langchain_core.runnables import chain
from dotenv import load_dotenv

from src.agents.chains.router import chain as router_chain
from src.agents.chains.executer import chain as executor_chain
from src.agents.chains.planner import chain as planner_chain
from src.agents.prompts.base import get_reference_files_prompt

load_dotenv()

@chain
async def agent_controller(parsed_data: dict) -> dict:
    messages = parsed_data["messages"]
    special_instructions = parsed_data["special_instructions"]
    reference_files = parsed_data["reference_files"]
    mode = parsed_data["mode"]
    
    try:
        # 1 Add Reference Files
        messages[-1].content = f"{messages[-1].content}\n{get_reference_files_prompt(reference_files)}"
        
        # 2. Determine Mode with smart router
        if mode == "auto":
            router_response = await router_chain.ainvoke({"messages": messages, "special_instructions": special_instructions})
            mode = router_response.content.strip().lower()

        # 3. Plan Mode
        if "execute" not in mode:
            response = await planner_chain.ainvoke({"messages": messages, "special_instructions": special_instructions})
            return {
                "message": {
                    "type": "assistant",
                    "content": response.content,
                },
                "mode": "planned"
            }
        
        else: # Default to execute mode
            response = await executor_chain.ainvoke({"messages": messages, "special_instructions": special_instructions})
            
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
