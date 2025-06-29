class DeveloperToolsPrompts:
    """Collection of prompts to analyze financial data."""

    TOOL_EXTRACTION_SYSTEM = """You are a financial analyzer. You will explore financial data, extract, use data and
    make assumptions based on the prompt."""

    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
"""
