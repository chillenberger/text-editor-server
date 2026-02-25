def get_system_prompt(base_role_instructions, special_instructions="{special_instructions}"): 
    return f"""
{base_role_instructions}

<special_instructions>
{special_instructions}
</special_instructions>

Final Reminder: User constraints must be followed unless they violate safety or the core integrity of the system.
"""

def get_reference_files_prompt(reference_files):
    if not reference_files:
        return ""

    return f"""
    <reference_files>
    I am currnetly viewing this file:
    {reference_files.pop(0)}
    I am referencing the following files and folders:
    {"\n".join(reference_files)}
    </reference_files>
    """