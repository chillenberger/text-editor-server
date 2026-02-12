def get_system_prompt(base_role_instructions, special_instructions="{special_instructions}"): 
    return f"""
{base_role_instructions}

<special_instructions>
{special_instructions}
</special_instructions>

Final Reminder: User constraints must be followed unless they violate safety or the core integrity of the system.
"""
