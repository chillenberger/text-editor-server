# Project Structure & LLM Reference Guide

This document defines the file structure and architectural context of the `co_doc_ai` project. Use this key to understand where logic resides and how components interact.

## 🏗 High-Level Architecture
This project serves as the **Python Server ("Brain")** for a "Split-Brain" AI assistant. 
- **Server (This Repo)**: Stateless. Receives `messages[]`, decides the next action (Plan, Execute, or Response), and returns it. **Never** executes tools directly; it only *requests* them.
- **Client (VS Code Extension)**: Stateful. Holds conversation history, performs actual file I/O and tool execution, and manages the loop.

---

## 📂 File Structure

### Root Directory
- **`main.py`**: The Entry Point.
    -   Sets up the `FastAPI` server.
    -   Exposes the `general_agent` runtime via `langserve`.
- **`ARCHITECTURE.md`**: Detailed conceptual documentation of the "Split-Brain" model.
- **`STRUCTURE.md`**: This file.
- **`agents.md`**: Developer instructions for creating/managing agents.
- **`.env`**: Configuration (API Keys, Model names, Temperatures).
- **`requirements.txt`**: Python package dependencies.
- **`tests/`**: Contains integration tests.

### Source Code (`src/`)

#### 🧠 Agents (`src/agents/`)
*The main entry points for different agent behaviors.*
- **`general.py`**: The primary `general_agent` implementation.
    -   **Role**: The "Orchestrator".
    -   **Flow**: Reconstructs state -> Routes request -> Invokes Chain -> Returns Response.

#### 🔗 Chains (`src/chains/`)
*Specialized "Micro-Brains" for specific cognitive tasks.*
- **`router.py`**: A classifier chain.
    -   **Input**: Conversation History.
    -   **Output**: `"PLAN"` (complex task) or `"EXECUTE"` (simple task).
- **`planner.py`**: A reasoning chain.
    -   **Input**: Request context.
    -   **Output**: A structured, step-by-step implementation plan (Markdown).
    -   **Constraint**: Cannot call tools. Pure reasoning.
- **`executer.py`**: An action chain.
    -   **Input**: Plan + History.
    -   **Output**: A **Tool Call** (to modify files) or a final answer.
    -   **Tools**: Has access to `client_tools`.

#### 📝 Prompts (`src/prompts/`)
*Prompt templates for the chains.*
- **`base.py`**: Base prompt templates and system messages.
- **`router.py`**: Prompts for the router chain.
- **`planner.py`**: Prompts for the planner chain.
- **`executer.py`**: Prompts for the executor chain.

#### 🛠 Tools (`src/tools/`)
*Interface definitions for Client capabilities.*
- **`client_tools.py`**:
    -   **Purpose**: Defines the *Schema* of tools available to the Agent.
    -   **Implementation**: **None**. These functions are empty (`pass`) or mocks.
    -   **Execution**: The *Client* (VS Code) sees the tool call name (e.g., `create_file`) and executes its own local implementation.
    -   **Available Tools**: `read_file`, `create_file`, `propose_file_change`, `get_workspace_structure`, etc.
