"""
OpenAI Connector
Handles communication with OpenAI API for intelligent decision-making
"""

from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import json

load_dotenv()


class OpenAIConnector:
    """
    Production-ready OpenAI connector with error handling
    """
    
    def __init__(self, model: str = "gpt-4o-mini"):
        """
        Initialize OpenAI connector
        
        Args:
            model: OpenAI model to use (gpt-4o-mini is cost-effective)
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        print(f"✓ Connected to OpenAI ({self.model})")
    
    def analyze_data_for_visualization(
        self,
        data_summary: str,
        columns: list
    ) -> Dict[str, Any]:
        """
        Ask OpenAI to analyze data and recommend best chart type
        
        Args:
            data_summary: String summary of the DataFrame
            columns: List of column names
            
        Returns:
            Dictionary with chart recommendations
        """
        try:
            prompt = f"""You are a data visualization expert. Analyze this data and recommend the best chart type.

Data Summary:
{data_summary}

Columns: {columns}

Based on this data, provide:
1. The best chart type (bar, line, or dual_axis)
2. Which columns should be on which axis
3. Brief reasoning for your choice

Respond in JSON format:
{{
    "chart_type": "bar|line|dual_axis",
    "x_column": "column_name",
    "y1_column": "column_name",
    "y2_column": "column_name or null",
    "reasoning": "brief explanation"
}}"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data visualization expert. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            recommendation = json.loads(response.choices[0].message.content)
            
            print("\n🤖 OpenAI Recommendation:")
            print(f"   Chart Type: {recommendation['chart_type']}")
            print(f"   Reasoning: {recommendation['reasoning']}")
            
            return recommendation
            
        except Exception as e:
            raise Exception(f"Error getting OpenAI recommendation: {str(e)}")
    
    def chat(
        self,
        prompt: str,
        system_message: Optional[str] = None
    ) -> str:
        """
        Simple chat interface with OpenAI
        
        Args:
            prompt: User message
            system_message: Optional system instructions
            
        Returns:
            OpenAI's response text
        """
        try:
            messages = []
            
            if system_message:
                messages.append({"role": "system", "content": system_message})
            
            messages.append({"role": "user", "content": prompt})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error in OpenAI chat: {str(e)}")


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("OPENAI CONNECTOR - Testing Connection")
    print("=" * 60)
    
    # Test connection
    connector = OpenAIConnector()
    
    # Test simple chat
    print("\n Testing simple chat...")
    response = connector.chat("Say 'Hello! OpenAI is connected.' in a friendly way.")
    print(f"\nOpenAI: {response}")
    
    print("\n" + "=" * 60)
    print(" OpenAI connection successful!")
    print("=" * 60)
