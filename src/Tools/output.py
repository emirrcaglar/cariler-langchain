from langchain.tools import BaseTool
import pandas as pd
from pydantic import Field, BaseModel
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import json

class ReportConfig(BaseModel):
    """Configuration for report generation with validation"""
    title: str = Field(..., description="The main title of the report")
    summary: str = Field(..., description="Executive summary of the report")
    metrics: Dict[str, Union[int, float, str]] = Field(default_factory=dict, description="Key performance metrics")
    data_sample: Optional[List[Dict[str, Any]]] = Field(default=None, description="Sample data as list of dictionaries")
    recommendations: List[str] = Field(default_factory=list, description="List of actionable recommendations")
    insights: List[str] = Field(default_factory=list, description="Key insights and findings")
    context: Optional[str] = Field(default=None, description="Additional context or background information")
    output_format: str = Field(default="comprehensive", description="Report format: 'executive', 'comprehensive', 'dashboard'")
    max_table_rows: int = Field(default=10, description="Maximum rows to show in data tables")

class ReportGeneratorTool(BaseTool):
    name: str = "report_generator"
    description: str = """
    Advanced report generator for creating professional markdown reports with multiple format options.
    
    Input should be a JSON string with the following structure:
    {
        "title": "Report Title",
        "summary": "Executive summary text",
        "metrics": {"Key Metric": "Value", "Another Metric": 123},
        "data_sample": [{"col1": "value1", "col2": "value2"}, ...],
        "recommendations": ["Recommendation 1", "Recommendation 2"],
        "insights": ["Key insight 1", "Key insight 2"],
        "context": "Additional background information",
        "output_format": "comprehensive|executive|dashboard",
        "max_table_rows": 10
    }
    
    Output formats:
    - 'executive': Concise summary with key metrics only
    - 'comprehensive': Full detailed report with all sections
    - 'dashboard': Metrics-focused with minimal narrative
    """
    
    df: pd.DataFrame = Field(..., description="The current DataFrame being analyzed")
    
    def _run(self, tool_input: str) -> str:
        try:
            # Parse and validate input
            data = json.loads(tool_input)
            config = ReportConfig(**data)
            
            # Generate report based on format
            if config.output_format == "executive":
                return self._generate_executive_report(config)
            elif config.output_format == "dashboard":
                return self._generate_dashboard_report(config)
            else:
                return self._generate_comprehensive_report(config)
                
        except json.JSONDecodeError as e:
            return f"❌ **Error**: Invalid JSON input - {str(e)}"
        except Exception as e:
            return f"❌ **Error**: Report generation failed - {str(e)}"
    
    async def _arun(self, tool_input: str):
        raise NotImplementedError("This tool does not support async execution.")
    
    def _generate_executive_report(self, config: ReportConfig) -> str:
        """Generate concise executive summary report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# 📊 {config.title}
*Generated on {timestamp}*

## Executive Summary
{config.summary}

## Key Metrics
{self._format_metrics_table(config.metrics)}

## Priority Actions
{self._format_recommendations_bullets(config.recommendations[:3])}

---
*Executive Summary Format - For detailed analysis, request comprehensive report*
"""
        return report.strip()
    
    def _generate_dashboard_report(self, config: ReportConfig) -> str:
        """Generate metrics-focused dashboard report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# 📈 {config.title} - Dashboard
*Updated: {timestamp}*

## Performance Metrics
{self._format_metrics_cards(config.metrics)}

## Status Overview
{config.summary}

## Data Sample
{self._format_data_table(config.data_sample, config.max_table_rows)}

## Action Items
{self._format_recommendations_numbered(config.recommendations)}

---
*Dashboard View - Refresh for latest metrics*
"""
        return report.strip()
    
    def _generate_comprehensive_report(self, config: ReportConfig) -> str:
        """Generate full detailed report"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# 📋 {config.title}
*Generated on {timestamp}*

## 1. Executive Summary
{config.summary}

## 2. Key Performance Metrics
{self._format_metrics_table(config.metrics)}

## 3. Data Analysis
{self._format_data_section(config.data_sample, config.max_table_rows)}

## 4. Key Insights
{self._format_insights(config.insights)}

## 5. Recommendations
{self._format_recommendations_detailed(config.recommendations)}

{self._format_context_section(config.context)}

---
*Comprehensive Report - All sections included*
"""
        return report.strip()
    
    def _format_metrics_table(self, metrics: Dict[str, Any]) -> str:
        """Format metrics as a clean table"""
        if not metrics:
            return "*No metrics available*"
        
        table = "| Metric | Value |\n|--------|-------|\n"
        for key, value in metrics.items():
            # Format numbers with commas
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
            else:
                formatted_value = str(value)
            table += f"| {key} | {formatted_value} |\n"
        
        return table
    
    def _format_metrics_cards(self, metrics: Dict[str, Any]) -> str:
        """Format metrics as dashboard cards"""
        if not metrics:
            return "*No metrics available*"
        
        cards = ""
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                formatted_value = f"{value:,.2f}" if isinstance(value, float) else f"{value:,}"
            else:
                formatted_value = str(value)
            cards += f"**{key}**: `{formatted_value}`  \n"
        
        return cards
    
    def _format_data_table(self, data_sample: Optional[List[Dict]], max_rows: int) -> str:
        """Format data sample as markdown table"""
        if not data_sample:
            return "*No data sample available*"
        
        try:
            df = pd.DataFrame(data_sample)
            if len(df) > max_rows:
                df = df.head(max_rows)
                truncated_note = f"\n*Showing first {max_rows} rows of {len(data_sample)} total records*"
            else:
                truncated_note = ""
            
            return df.to_markdown(index=False) + truncated_note
        except Exception as e:
            return f"*Error formatting data table: {str(e)}*"
    
    def _format_data_section(self, data_sample: Optional[List[Dict]], max_rows: int) -> str:
        """Format comprehensive data analysis section"""
        if not data_sample:
            return "*No data available for analysis*"
        
        try:
            df = pd.DataFrame(data_sample)
            
            section = f"**Dataset Overview:**\n"
            section += f"- Total Records: {len(data_sample)}\n"
            section += f"- Columns: {len(df.columns)}\n\n"
            
            section += "**Sample Data:**\n"
            section += self._format_data_table(data_sample, max_rows)
            
            return section
        except Exception as e:
            return f"*Error in data analysis: {str(e)}*"
    
    def _format_insights(self, insights: List[str]) -> str:
        """Format insights as bullet points"""
        if not insights:
            return "*No specific insights identified*"
        
        formatted = ""
        for i, insight in enumerate(insights, 1):
            formatted += f"**{i}.** {insight}\n\n"
        
        return formatted.strip()
    
    def _format_recommendations_bullets(self, recommendations: List[str]) -> str:
        """Format recommendations as bullet points"""
        if not recommendations:
            return "*No recommendations available*"
        
        return "\n".join(f"• {rec}" for rec in recommendations)
    
    def _format_recommendations_numbered(self, recommendations: List[str]) -> str:
        """Format recommendations as numbered list"""
        if not recommendations:
            return "*No action items*"
        
        return "\n".join(f"{i}. {rec}" for i, rec in enumerate(recommendations, 1))
    
    def _format_recommendations_detailed(self, recommendations: List[str]) -> str:
        """Format recommendations with detailed formatting"""
        if not recommendations:
            return "*No recommendations available*"
        
        formatted = ""
        for i, rec in enumerate(recommendations, 1):
            priority = "🔴 High" if i <= 2 else "🟡 Medium" if i <= 4 else "🟢 Low"
            formatted += f"### {i}. {rec}\n**Priority:** {priority}\n\n"
        
        return formatted.strip()
    
    def _format_context_section(self, context: Optional[str]) -> str:
        """Format context section if provided"""
        if not context:
            return ""
        
        return f"""
## 6. Additional Context
{context}
"""

# Usage example for reference
def example_usage():
    """Example of how to use the improved report generator"""
    sample_input = {
        "title": "Monthly Sales Analysis",
        "summary": "Sales performance showed strong growth in Q1 with notable improvements in customer retention.",
        "metrics": {
            "Total Revenue": 125000.50,
            "Growth Rate": 15.2,
            "Customer Count": 1250,
            "Avg Order Value": 100.0
        },
        "data_sample": [
            {"Product": "Widget A", "Sales": 5000, "Profit": 1500},
            {"Product": "Widget B", "Sales": 3000, "Profit": 900}
        ],
        "recommendations": [
            "Increase marketing spend in high-performing segments",
            "Implement customer loyalty program",
            "Optimize pricing strategy for Widget A"
        ],
        "insights": [
            "Customer retention improved by 25% compared to last quarter",
            "Widget A shows highest profit margin potential"
        ],
        "context": "Analysis based on Q1 2024 data with seasonal adjustments applied",
        "output_format": "comprehensive",
        "max_table_rows": 10
    }
    
    return json.dumps(sample_input, indent=2)