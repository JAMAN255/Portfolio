

import pandas as pd

class Data:
    @staticmethod
    def import_data(file_path: str, sheet_name: str = 0):
        """
        Import data from an Excel file.
        
        Args:
            file_path (str): Path to the Excel file
            sheet_name (str or int): Sheet name or index to read. Default is 0 (first sheet)
            
        Returns:
            pd.DataFrame: Data from the Excel file, or None if import fails
        """
        try:
            print(f"Importing data from {file_path}...")
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Successfully imported {len(df)} rows and {len(df.columns)} columns")
            return df
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return None
        except Exception as e:
            print(f"Error importing data: {e}")
            return None

    @staticmethod
    def export_data(df: pd.DataFrame, file_path: str, sheet_name: str = "Sheet1"):
        """
        Export data to an Excel file.
        
        Args:
            df (pd.DataFrame): DataFrame to export
            file_path (str): Path where the Excel file will be saved
            sheet_name (str): Name of the sheet in the Excel file. Default is "Sheet1"
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        try:
            print(f"Exporting data to {file_path}...")
            df.to_excel(file_path, sheet_name=sheet_name, index=False)
            print(f"Successfully exported {len(df)} rows and {len(df.columns)} columns")
            return True
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False