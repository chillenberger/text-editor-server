# Agent Instructions

## Environment Setup
- **Language:** Python 3.10+
- **Virtual Environment:** Always use the `.venv` directory in the project root.
- **Activation:** Run `source .venv/bin/activate` (Linux/macOS) or `.venv\Scripts\activate` (Windows) before running any code.

## Package Management
- Install dependencies using: `pip install -r requirements.txt`
- If a new library is needed, add it to `requirements.txt` and install it within the venv.

## Code Execution & Standards
- Use `python3` for execution.
- Ensure all Python code is compatible with Python 3.
- Do not use Python 2 syntax (e.g., use `print()` not `print`).
- All scripts must be executed within the activated virtual environment.
- Run tests using: `pytest`

## Project Structure
- Source code: `src/`
- Tests: `tests/`
