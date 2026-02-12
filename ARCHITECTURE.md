# Project Architecture & Mental Model

## Core Concept: The "Split-Brain" Agent

This project implements an AI assistant where the **Brain (Inference)** is decoupled from the **Body (Execution)**.

-   **Server (Python)**: The "Brain". It is stateless. It receives context, decides the next step, and returns it. It *never* executes tools or loops itself.
-   **Client (VS Code)**: The "Body". It is stateful. It holds the conversation history, executes the tools requested by the server, and loops back to the server with the results.

---

## 1. The Python Server (`src/agents/general.py`)

**What it IS:**
*   A **Stateless Inference Endpoint**.
*   An **Orchestrator** that routes requests to specialized chains.
*   A **Tool Requester** (decides which tools to call, but doesn't run them).

**What it IS NOT:**
*   An "Agent" (in the traditional loop sense).
*   Stateful (it does not store history in a DB).
*   Autonomous (it cannot "go off and do things" on its own).

### Request/Response Cycle
1.  **Input**:
    *   `messages[]`: Conversation history.
    *   `new_message`: The latest user or tool message.
    *   `mode`: `"plan"`, `"execute"`, or `"auto"` (default).
    *   `special_instructions`: Optional constraints.

2.  **Processing** (`src/agents/general.py`):
    *   **Reconstruct History**: Converts raw JSON into LangChain Message objects.
    *   **Determine Mode**:
        *   **If Mode = "auto"**: Uses `src/chains/router.py` to classify intent as `"PLAN"` or `"EXECUTE"`.
        *   **If Mode = "plan"**: Invokes `src/chains/planner.py` to generate a structured plan.
        *   **If Mode = "execute"**: Invokes `src/chains/executer.py` to generate a tool call or final response.

3.  **Output**: Returns **ONE** of:
    *   `text`: The Plan (in plan mode) or a conversational response.
    *   `tool_call`: A structured request to run a specific function (e.g., `create_file`).

---

## 2. The Client (VS Code Extension)

**Responsibilities:**
*   **State Management**: Maintains the `messages[]` array (History).
*   **Tool Execution**: When the Server returns a `tool_call`, the Client actually runs the code (e.g., performs the file IO).
*   **The Loop**:
    1.  Send History to Server -> Get Response.
    2.  If Response is `tool_call` -> Execute Tool -> Append Result to History -> **Loop Back to 1**.
    3.  If Response is `text` -> Show to User -> Wait for User Input.

---

## 3. How to Describe This to LLMs

When asking LLMs for help with this codebase, use the following framing to avoid getting "Agent Framework" advice:

> "I am building a **Stateless Tool-Calling Chain** using standard LangChain primitives.
>
> The Python server handles **single-turn inference only**. It takes a history of messages and returns a single response or tool call. It does **not** manage memory or execute loops; the client (VS Code) handles the execution loop and state.
>
> Please treat this as a simple **Request-Response** architecture, not an autonomous agent framework like LangGraph or AgentExecutor."
