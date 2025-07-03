from langchain.tools import BaseTool
import pandas as pd
from pydantic import Field

class ReportGeneratorTool(BaseTool):
    name: str = "report_generator"
    description: str = """
    Useful for regenerating comprehensive markdown reports based on provided data and summaries.
    Input should be a JSON string with the following keys:
    - 'title': The main title of the report.
    - 'summary': A summary of the report.
    - 'metrics': A dictionary of key metrics (e.g., {'Total Rows':
    100, 'Filtered Rows': 50}).
    - 'data_sample_df': A pandas DataFrame to be included as a markdown table.
    - 'recommendations': Any recommendations or next steps.
    """
    df: pd.DataFrame = Field(..., description="The current DataFrame being analyzed")

    def _run(self, tool_input: str) -> str:
        import json
        try:
            data = json.loads(tool_input)
            title = data.get("title", "Generated Report")
            summary = data.get("summary", "No summary provided.")
            metrics = data.get("metrics", {})
            data_sample_list = data.get("data_sample")
            recommendations = data.get("recommendations", "No recommendations provided.")

            data_sample_df = pd.DataFrame(data_sample_list) if data_sample_list else pd.DataFrame()
            markdown_report = generate_markdown_report(
                title=title,
                summary=summary,
                metrics=metrics,
                data_sample_df=data_sample_df,
                recommendations=recommendations
            )
            return markdown_report
        except Exception as e:
            return f"Error generating report: {str(e)}"

    async def _arun(self, tool_input: str):
        raise NotImplementedError("This tool does not support async execution.")



def generate_markdown_report(title, summary, metrics, data_sample_df, recommendations):
    """
    Generates a markdown formatted report.

    Args:
        title (str): The main title of the report.
        summary (str): A summary of the report.
        metrics (dict): A dictionary of key metrics (e.g., {'Total Rows': 100, 'Filtered Rows': 50}).
        data_sample_df (pd.DataFrame): A pandas DataFrame to be included as a markdown table.
        recommendations (str): Any recommendations or next steps.

    Returns:
        str: A markdown formatted string.
    """
    import pandas as pd

    markdown_output = f"""
    # {title}

    ## Summary
    {summary}

    ## Key Metrics
    """

    for key, value in metrics.items():
        markdown_output += f"- {key}: {value}\n"

    markdown_output += f"""

    ## Data Sample
    {data_sample_df.to_markdown(index=False)}

    ## Recommendations
    {recommendations}
    """

    return markdown_output