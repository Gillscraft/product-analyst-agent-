"""
Intelligent Agent
Combines Google Sheets, Chart Building, and OpenAI for smart visualization
"""

from sheets_connector import SheetsConnector
from Chart_builder import ChartBuilder
from openai_connector import OpenAIConnector
import pandas as pd


class IntelligentAgent:
    """
    Agentic workflow that uses OpenAI to make intelligent decisions
    """
    
    def __init__(self):
        """Initialize all tools"""
        print("🤖 Initializing Intelligent Agent...")
        self.sheets = SheetsConnector()
        self.charts = ChartBuilder()
        self.ai = OpenAIConnector()
        print("✓ All systems ready!\n")
    
    def analyze_and_visualize(self, sheet_id: str = None, title: str = None):
        """
        Complete workflow: Fetch data → Ask AI → Create chart
        
        Args:
            sheet_id: Optional Google Sheet ID
            title: Optional chart title
        """
        print("=" * 60)
        print("INTELLIGENT VISUALIZATION WORKFLOW")
        print("=" * 60)
        
        # Step 1: Fetch data
        print("\n📊 Step 1: Fetching data from Google Sheets...")
        df = self.sheets.fetch_data(sheet_id)
        print(f"   Retrieved {len(df)} rows")
        # debugging 
        # ADD THESE DEBUG LINES:
        print(f"\n🔍 DEBUG - Actual columns in sheet: {df.columns.tolist()}")
        print(f"🔍 DEBUG - Data preview:")
        print(df.head())
        
        # Step 2: Prepare data summary for AI
        print("\n🧠 Step 2: Asking OpenAI for visualization recommendation...")
        data_summary = df.describe().to_string()
        columns = df.columns.tolist()
        
        # Get AI recommendation
        recommendation = self.ai.analyze_data_for_visualization(
            data_summary,
            columns
        )
        
        # Step 3: Create chart based on AI recommendation
        print(f"\n📈 Step 3: Creating {recommendation['chart_type']} chart...")
        
        if recommendation['chart_type'] == 'dual_axis':
            chart_path = self.charts.create_dual_axis_chart(
                df,
                x_column=recommendation['x_column'],
                y1_column=recommendation['y1_column'],
                y2_column=recommendation['y2_column'],
                title=title or "AI-Generated Visualization"
            )
        elif recommendation['chart_type'] == 'bar':
            chart_path = self.charts.create_bar_chart(
                df,
                x_column=recommendation['x_column'],
                y_column=recommendation['y1_column'],
                title=title or "AI-Generated Visualization"
            )
        else:  # line
            y_columns = [col for col in columns if col != recommendation['x_column']]
            chart_path = self.charts.create_line_chart(
                df,
                x_column=recommendation['x_column'],
                y_columns=y_columns,
                title=title or "AI-Generated Visualization"
            )
        
        print("\n" + "=" * 60)
        print(f"✅ SUCCESS!")
        print(f"   Chart saved: {chart_path}")
        print(f"   AI's reasoning: {recommendation['reasoning']}")
        print("=" * 60)
        
        return chart_path


# Example usage
if __name__ == "__main__":
    # Create the intelligent agent
    agent = IntelligentAgent()
    
    # Let the AI decide how to visualize your data
    chart = agent.analyze_and_visualize(title="Q3 Sales Analysis")
    
    print(f"\n Open your chart: {chart}")
