import pandas as pd
import os
import chardet

class DataLoader:
    def __init__(self, directory):
        self.directory = directory
        self.dataframes = {}

    def detect_encoding(self, file_path):
        """Detect the encoding of a file using chardet."""
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding_result = chardet.detect(data)
            return encoding_result.get('encoding', 'utf-8')  # Default to 'utf-8' if detection fails

    def load_all_csvs(self, delimiter=None):
        """
        Automatically detect encoding and load all CSV files from the directory.
        Parameters:
            - delimiter: Delimiter to use. Automatically detects if not provided.
        Returns:
            A dictionary of DataFrames.
        """
        for filename in os.listdir(self.directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.directory, filename)
                key = os.path.splitext(filename)[0]

                try:
                    # Detect encoding
                    encoding = self.detect_encoding(filepath)
                    #print(f"{filename}: encoding = {encoding}")

                    # Detect delimiter automatically if not specified
                    if delimiter is None:
                        with open(filepath, 'r', encoding=encoding) as file:
                            sample = file.read(1024)
                            delimiter = ',' if ',' in sample else ';'

                    # Load CSV with detected encoding and delimiter
                    df = pd.read_csv(filepath, encoding=encoding, delimiter=delimiter)

                    # Normalize column names (remove whitespace, fix delimiters)
                    df.columns = df.columns.str.strip()

                    # Convert all object columns to string
                    for col in df.select_dtypes(include=['object']).columns:
                        df[col] = df[col].astype(str)
                    # Ensure numeric columns are integers
                    for col in df.select_dtypes(include=['float64']).columns:
                        df[col] = df[col].fillna(0).astype(int)  # Fill NaN with 0 and convert to int


                    self.dataframes[key] = df
                    print(f"{filename} loaded successfully.")
                except Exception as e:
                    print(f"{filename} error: {e}")

        return self.dataframes

    def get_preview(self, key=None, rows=5):
        """
        Print a preview of a specific DataFrame or all DataFrames, including column types.
        Parameters:
            - key: The key of the dataset to preview. If None, previews all datasets.
            - rows: Number of rows to display in the preview.
        """
        if key:
            if key in self.dataframes:
                df = self.dataframes[key]
                print(f"\nPreview of '{key}':")
                print("\nColumn Types:")
                print(df.dtypes)  # Print the data types of each column
                print("\nPreview:")
                print(df.head(rows))  # Print the first 'rows' rows of the dataset
            else:
                print(f"No dataset found with key: {key}, so preview cannot be made.")
        else:
            print("Preview of all datasets:")
            for dataset_key, df in self.dataframes.items():
                print(f"\n--- {dataset_key} ---")
                print("Column Types:")
                print(df.dtypes)  # Print the data types of each column
                print("\nPreview:")
                print(df.head(rows))  # Print the first 'rows' rows of the dataset

