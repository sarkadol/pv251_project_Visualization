import pandas as pd
import os
import chardet
import io

class DataLoader:
    def __init__(self, directory):
        self.directory = directory
        self.dataframes_by_type = {
            'O2': {},
            'S2': {},
            'V2': {}
        }
        self.merged_dataframes = {
            'O2': None,
            'S2': None,
            'V2': None
        }

    def detect_encoding(self, file_path):
        """Detect the encoding of a file using chardet."""
        with open(file_path, 'rb') as f:
            data = f.read()
            encoding_result = chardet.detect(data)
            return encoding_result.get('encoding', 'utf-8')  # Default to 'utf-8' if detection fails

    def load_all_csvs(self, delimiter=None):
        """
        Load all CSV files, categorize them by type, and optionally merge them.
        """
        for filename in os.listdir(self.directory):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.directory, filename)

                # Determine the dataset type based on the filename
                if filename.startswith('O2'):
                    dataset_type = 'O2'
                elif filename.startswith('S2'):
                    dataset_type = 'S2'
                elif filename.startswith('V2'):
                    dataset_type = 'V2'
                else:
                    continue  # Skip files that don't match known types

                try:
                    # Detect encoding
                    encoding = self.detect_encoding(filepath)
                    print(f"{filename}: encoding = {encoding}")

                    # Read file content with error handling
                    with open(filepath, 'r', encoding=encoding, errors='replace') as file:
                        file_content = file.read()

                    # Detect delimiter automatically if not specified
                    if delimiter is None:
                        delimiter = ',' if ',' in file_content[:1024] else ';'

                    # Load the CSV using StringIO
                    df = pd.read_csv(io.StringIO(file_content), delimiter=delimiter)

                    # Normalize column names
                    df.columns = df.columns.str.strip()

                    # Add a 'Year' column if not already present
                    if 'Year' not in df.columns:
                        df['Year'] = int(filename.split('_')[-1].split('.')[0])  # Extract year from filename

                    # Store the DataFrame in the appropriate category
                    key = os.path.splitext(filename)[0]
                    self.dataframes_by_type[dataset_type][key] = df
                    #print(f"{filename} loaded successfully.")

                except Exception as e:
                    print(f"{filename} error: {e}")

        # Merge datasets of each type
        for dataset_type, dataframes in self.dataframes_by_type.items():
            if dataframes:
                self.merged_dataframes[dataset_type] = pd.concat(dataframes.values(), ignore_index=True)
        return self.dataframes_by_type  # Return the categorized datasets


    def get_merged_dataframe(self, dataset_type):
        """
        Get the merged DataFrame for a specific dataset type.
        """
        if dataset_type in self.merged_dataframes:
            return self.merged_dataframes[dataset_type]
        else:
            raise ValueError(f"Dataset type '{dataset_type}' not recognized.")

    def get_preview(self, key=None, dataset_type=None, rows=5):
        """
        Print a preview of a specific DataFrame or all DataFrames, including column types.
        Parameters:
            - key: The key of the dataset to preview. If None, previews all datasets of the given type.
            - dataset_type: The type of dataset to preview ('O2', 'S2', 'V2'). If None, previews all types.
            - rows: Number of rows to display in the preview.
        """
        if dataset_type:
            if dataset_type not in self.dataframes_by_type:
                print(f"No datasets found for type '{dataset_type}'.")
                return

            if key:
                # Preview a specific dataset within the given type
                if key in self.dataframes_by_type[dataset_type]:
                    df = self.dataframes_by_type[dataset_type][key]
                    print(f"\nPreview of '{key}' ({dataset_type}):")
                    #print("\nColumn Types:")
                    #print(df.dtypes)  # Print the data types of each column
                    print("\nPreview:")
                    print(df.head(rows))  # Print the first 'rows' rows of the dataset
                else:
                    print(f"No dataset found with key: {key} in type '{dataset_type}'.")
            else:
                # Preview all datasets within the given type
                print(f"Preview of all datasets in type '{dataset_type}':")
                for dataset_key, df in self.dataframes_by_type[dataset_type].items():
                    print(f"\n--- {dataset_key} ---")
                    #print("Column Types:")
                    #print(df.dtypes)  # Print the data types of each column
                    print("\nPreview:")
                    print(df.head(rows))  # Print the first 'rows' rows of the dataset
        else:
            # Preview all datasets across all types
            print("Preview of all datasets across all types:")
            for dtype, datasets in self.dataframes_by_type.items():
                print(f"\n--- Dataset Type: {dtype} ---")
                for dataset_key, df in datasets.items():
                    print(f"\n--- {dataset_key} ---")
                    #print("Column Types:")
                    #print(df.dtypes)  # Print the data types of each column
                    print("\nPreview:")
                    print(df.head(rows))  # Print the first 'rows' rows of the dataset
