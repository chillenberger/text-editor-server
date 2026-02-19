from langchain_core.tools import StructuredTool
# -------------------
# Tool schemas (NO implementation)
# -------------------
def change_file_location(old_path: str, new_path: str):
    """Rename a file in the user's workspace."""
    pass

change_file_location_tool = StructuredTool.from_function(
    change_file_location,
    name="change_file_location",
    description=(
        "Rename a file in the VS Code workspace. "
        "You must know the full source path and destination path."
    ),
)

def get_workspace_structure():
    """Get the structure of the workspace."""
    pass

get_workspace_structure_tool = StructuredTool.from_function(
    get_workspace_structure,
    name="get_workspace_structure",
    description="Return the full workspace directory tree.",
)

def create_file(path: str, content: str = ""):
    """Create a file in the user's workspace."""
    pass

create_file_tool = StructuredTool.from_function(
    create_file,
    name="create_file",
    description="Create a file in the text editor workspace.",
)

def delete_file(path: str):
    """Delete a file in the user's workspace."""
    pass

delete_file_tool = StructuredTool.from_function(
    delete_file,
    name="delete_file",
    description="Delete a file in the VS Code workspace.",
)

def read_file(path: str):
    """Read a file in the user's workspace."""
    pass

read_file_tool = StructuredTool.from_function(
    read_file,
    name="read_file",
    description="Read a text file from the user's workspace. ",
)

def propose_file_change(file_path: str, original_content: str, proposed_content: str, description: str):
    """Propose changes to a file in the user's workspace."""
    pass

propose_file_change_tool = StructuredTool.from_function(
    propose_file_change,
    name="propose_file_change",
    description="Propose changes to a file in the text editor workspace.",
)
