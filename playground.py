PROMPT_TEMPLATE: str = """
    Context: {context}
    Review the test cases and provide one critical comments:
    """
    
print(PROMPT_TEMPLATE.format(context=123))