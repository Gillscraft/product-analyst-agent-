"""
Google Sheets Connector Tool
Fetches data from Google Sheets with proper error handling
"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict, Optional
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


class SheetsConnector:
    """
    A production-ready Google Sheets connector with error handling
    and type safety
    """
    
    def __init__(self, credentials_path: str = "credentials.json"):
        """
        Initialize the Google Sheets connector
        
        Args:
            credentials_path: Path to Google service account JSON
        """
        self.credentials_path = credentials_path
        self.client = None
        self._authenticate()
    
    def _authenticate(self) -> None:
        """Authenticate with Google Sheets API"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_path, 
                scope
            )
            self.client = gspread.authorize(creds)
            print("✓ Successfully authenticated with Google Sheets")
        except FileNotFoundError:
            raise Exception(f"Credentials file not found: {self.credentials_path}")
        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")
    
    def fetch_data(
        self, 
        sheet_id: Optional[str] = None,
        worksheet_name: str = "Sheet1"
    ) -> pd.DataFrame:
        """
        Fetch data from Google Sheet and return as pandas DataFrame
        
        Args:
            sheet_id: Google Sheet ID (uses env variable if not provided)
            worksheet_name: Name of the worksheet to fetch
            
        Returns:
            pandas DataFrame with the sheet data
        """
        try:
            # Use provided sheet_id or fall back to environment variable
            sheet_id = sheet_id or os.getenv('GOOGLE_SHEET_ID')
            
            if not sheet_id:
                raise ValueError("No sheet ID provided and GOOGLE_SHEET_ID not in .env")
            
            # Open the sheet
            sheet = self.client.open_by_key(sheet_id)
            worksheet = sheet.worksheet(worksheet_name)
            
            # Get all values
            data = worksheet.get_all_records()
            
            if not data:
                raise ValueError(f"No data found in worksheet: {worksheet_name}")
            
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            print(f"✓ Successfully fetched {len(df)} rows from {worksheet_name}")
            return df
            
        except gspread.exceptions.WorksheetNotFound:
            raise Exception(f"Worksheet '{worksheet_name}' not found")
        except gspread.exceptions.SpreadsheetNotFound:
            raise Exception(f"Spreadsheet with ID '{sheet_id}' not found")
        except Exception as e:
            raise Exception(f"Error fetching data: {str(e)}")
    
    def get_worksheet_names(self, sheet_id: Optional[str] = None) -> List[str]:
        """
        Get all worksheet names in a spreadsheet
        
        Args:
            sheet_id: Google Sheet ID
            
        Returns:
            List of worksheet names
        """
        try:
            sheet_id = sheet_id or os.getenv('GOOGLE_SHEET_ID')
            sheet = self.client.open_by_key(sheet_id)
            return [ws.title for ws in sheet.worksheets()]
        except Exception as e:
            raise Exception(f"Error getting worksheet names: {str(e)}")


# Example usage
if __name__ == "__main__":
    # Initialize connector
    connector = SheetsConnector()
    
    # Fetch data
    df = connector.fetch_data()
    
    # Display results
    print("\nData Preview:")
    print(df.head())
    print(f"\nShape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
