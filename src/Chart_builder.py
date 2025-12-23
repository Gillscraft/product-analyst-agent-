"""
Chart Builder Tool
Automatically creates visualizations from pandas DataFrames with intelligent chart selection
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional, List, Tuple
import os
from datetime import datetime

# Set style for professional-looking charts
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


class ChartBuilder:
    """
    Production-ready chart generation with automatic chart type selection
    and intelligent dual-axis detection
    """
    
    def __init__(self, output_dir: str = "charts"):
        """
        Initialize chart builder
        
        Args:
            output_dir: Directory to save generated charts
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self) -> None:
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ Created charts directory: {self.output_dir}")
    
    def _save_chart(self, filename: str) -> str:
        """
        Save chart and return filepath
        
        Args:
            filename: Name for the chart file
            
        Returns:
            Full path to saved chart
        """
        filepath = os.path.join(self.output_dir, filename)
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"✓ Chart saved: {filepath}")
        return filepath
    
    def _detect_chart_type(self, df: pd.DataFrame) -> Tuple[str, dict]:
        """
        Intelligently detect the best chart type based on data characteristics
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (chart_type, chart_config)
        """
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if len(numeric_cols) == 0:
            raise ValueError("No numeric columns found for visualization")
        
        # Detect if we need dual axis by checking:
        # 1. Do we have 2+ numeric columns?
        # 2. Are their scales very different? (order of magnitude)
        if len(numeric_cols) >= 2:
            col1_mean = df[numeric_cols[0]].mean()
            col2_mean = df[numeric_cols[1]].mean()
            
            # If one column is 10x+ larger than the other, use dual axis
            ratio = max(col1_mean, col2_mean) / min(col1_mean, col2_mean)
            
            if ratio >= 10:
                print(f"🧠 Detected large scale difference (ratio: {ratio:.1f}x)")
                print(f"   → Using dual-axis chart for better visualization")
                
                return "dual_axis", {
                    "x_column": df.columns[0],
                    "y1_column": numeric_cols[0],
                    "y2_column": numeric_cols[1],
                    "y1_label": numeric_cols[0],
                    "y2_label": numeric_cols[1]
                }
        
        # If columns have similar keywords (revenue/sales vs customers/users), use dual axis
        keywords_large = ['revenue', 'sales', 'income', 'profit', 'amount']
        keywords_count = ['customer', 'user', 'count', 'total', 'number']
        
        col_names_lower = [col.lower() for col in numeric_cols]
        has_large = any(kw in col for col in col_names_lower for kw in keywords_large)
        has_count = any(kw in col for col in col_names_lower for kw in keywords_count)
        
        if has_large and has_count and len(numeric_cols) >= 2:
            print("🧠 Detected revenue/customer pattern")
            print("   → Using dual-axis chart to show both metrics clearly")
            
            large_col = [col for col in numeric_cols if any(kw in col.lower() for kw in keywords_large)][0]
            count_col = [col for col in numeric_cols if any(kw in col.lower() for kw in keywords_count)][0]
            
            return "dual_axis", {
                "x_column": df.columns[0],
                "y1_column": large_col,
                "y2_column": count_col,
                "y1_label": large_col,
                "y2_label": count_col
            }
        
        # Single numeric column - use bar chart
        if len(numeric_cols) == 1:
            print("🧠 Single metric detected")
            print("   → Using bar chart")
            
            return "bar", {
                "x_column": df.columns[0],
                "y_column": numeric_cols[0]
            }
        
        # Multiple numeric columns with similar scales - use line chart
        print("🧠 Multiple metrics with similar scales")
        print("   → Using line chart for trend comparison")
        
        return "line", {
            "x_column": df.columns[0],
            "y_columns": numeric_cols
        }
    
    def create_bar_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_column: str,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Create a bar chart from DataFrame
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis
            y_column: Column for y-axis
            title: Chart title
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        try:
            plt.figure(figsize=(10, 6))
            
            # Create bar chart
            ax = sns.barplot(data=df, x=x_column, y=y_column, palette="viridis")
            
            # Customize
            plt.title(title or f"{y_column} by {x_column}", fontsize=14, fontweight='bold')
            plt.xlabel(x_column, fontsize=12)
            plt.ylabel(y_column, fontsize=12)
            plt.xticks(rotation=45, ha='right')
            
            # Add value labels on bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%.0f')
            
            # Save
            filename = filename or f"bar_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            return self._save_chart(filename)
            
        except Exception as e:
            raise Exception(f"Error creating bar chart: {str(e)}")
    
    def create_line_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y_columns: List[str],
        title: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Create a line chart from DataFrame
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis
            y_columns: List of columns for y-axis (can plot multiple lines)
            title: Chart title
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        try:
            plt.figure(figsize=(12, 6))
            
            # Plot each y column
            for col in y_columns:
                plt.plot(df[x_column], df[col], marker='o', label=col, linewidth=2)
            
            # Customize
            plt.title(title or f"Trend Analysis", fontsize=14, fontweight='bold')
            plt.xlabel(x_column, fontsize=12)
            plt.ylabel("Value", fontsize=12)
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            
            # Save
            filename = filename or f"line_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            return self._save_chart(filename)
            
        except Exception as e:
            raise Exception(f"Error creating line chart: {str(e)}")
    
    def create_dual_axis_chart(
        self,
        df: pd.DataFrame,
        x_column: str,
        y1_column: str,
        y2_column: str,
        y1_label: Optional[str] = None,
        y2_label: Optional[str] = None,
        title: Optional[str] = None,
        filename: Optional[str] = None
    ) -> str:
        """
        Create a chart with two y-axes for metrics with different scales
        
        Args:
            df: Input DataFrame
            x_column: Column for x-axis (e.g., "Month")
            y1_column: Column for left y-axis (e.g., "Revenue")
            y2_column: Column for right y-axis (e.g., "Customers")
            y1_label: Label for left y-axis
            y2_label: Label for right y-axis
            title: Chart title
            filename: Output filename
            
        Returns:
            Path to saved chart
        """
        try:
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
            y1_label = y1_label or y1_column
            y2_label = y2_label or y2_column
            
            # Plot first y-axis (typically larger values like Revenue) - Bar chart
            color1 = '#2E86AB'
            ax1.bar(df[x_column], df[y1_column], color=color1, alpha=0.7, label=y1_label)
            ax1.set_xlabel(x_column, fontsize=12, fontweight='bold')
            ax1.set_ylabel(y1_label, color=color1, fontsize=12, fontweight='bold')
            ax1.tick_params(axis='y', labelcolor=color1)
            
            # Format y1 axis labels (add $ if it's revenue/sales)
            if any(kw in y1_column.lower() for kw in ['revenue', 'sales', 'income', 'profit']):
                ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
            
            # Add value labels on bars
            for i, v in enumerate(df[y1_column]):
                if any(kw in y1_column.lower() for kw in ['revenue', 'sales', 'income', 'profit']):
                    label = f'${v:,.0f}'
                else:
                    label = f'{v:,.0f}'
                ax1.text(i, v, label, ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            # Create second y-axis (typically counts like Customers) - Line chart
            ax2 = ax1.twinx()
            color2 = '#A23B72'
            ax2.plot(df[x_column], df[y2_column], color=color2, marker='o', 
                    linewidth=3, markersize=8, label=y2_label)
            ax2.set_ylabel(y2_label, color=color2, fontsize=12, fontweight='bold')
            ax2.tick_params(axis='y', labelcolor=color2)
            
            # Add value labels on line
            for i, v in enumerate(df[y2_column]):
                ax2.text(i, v, f'{v:,.0f}', ha='center', va='bottom', 
                        color=color2, fontweight='bold', fontsize=9)
            
            # Title and grid
            plt.title(title or f"{y1_label} and {y2_label} Analysis", 
                     fontsize=14, fontweight='bold', pad=20)
            ax1.grid(True, alpha=0.3, linestyle='--')
            plt.xticks(rotation=45, ha='right')
            
            # Add legends
            lines1, labels1 = ax1.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
            
            # Save
            filename = filename or f"dual_axis_chart_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            return self._save_chart(filename)
            
        except Exception as e:
            raise Exception(f"Error creating dual axis chart: {str(e)}")
    
    def auto_visualize(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None
    ) -> str:
        """
        Automatically choose best visualization based on data characteristics
        Uses intelligent detection for:
        - Scale differences between metrics
        - Revenue/customer patterns
        - Single vs multiple metrics
        
        Args:
            df: Input DataFrame
            title: Chart title
            
        Returns:
            Path to saved chart
        """
        print("\n🤖 Analyzing data to determine best visualization...")
        print(f"   Columns: {df.columns.tolist()}")
        print(f"   Rows: {len(df)}")
        
        # Detect best chart type
        chart_type, config = self._detect_chart_type(df)
        
        # Create the appropriate chart
        if chart_type == "dual_axis":
            return self.create_dual_axis_chart(
                df,
                config["x_column"],
                config["y1_column"],
                config["y2_column"],
                config["y1_label"],
                config["y2_label"],
                title=title
            )
        elif chart_type == "bar":
            return self.create_bar_chart(
                df,
                config["x_column"],
                config["y_column"],
                title=title
            )
        else:  # line
            return self.create_line_chart(
                df,
                config["x_column"],
                config["y_columns"],
                title=title
            )


# Example usage
if __name__ == "__main__":
    from sheets_connector import SheetsConnector
    
    print("=" * 60)
    print("CHART BUILDER - Intelligent Visualization System")
    print("=" * 60)
    
    print("\n Step 1: Fetching data from Google Sheets...")
    connector = SheetsConnector()
    df = connector.fetch_data()
    
    print("\n Step 2: Creating intelligent visualization...")
    chart_builder = ChartBuilder()
    
    # Let the tool decide the best chart type automatically
    chart_path = chart_builder.auto_visualize(df, title="Sales Performance Analysis")
    
    print("\n" + "=" * 60)
    print(f" SUCCESS: Chart created at {chart_path}")
    print("=" * 60)
