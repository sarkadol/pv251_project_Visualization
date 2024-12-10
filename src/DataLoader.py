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
        self.merged_dataframe = None  # Store the merged DataFrame


    def detect_encoding(self, file_path):
            """Detect the encoding of a file using chardet."""
            with open(file_path, 'rb') as f:
                data = f.read()
                encoding_result = chardet.detect(data)
                return encoding_result.get('encoding', 'utf-8')  # Default to 'utf-8' if detection fails

    def load_all_csvs(self, delimiter=None):
        """
        Load all CSV files, categorize them by type.
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

                except Exception as e:
                    print(f"{filename} error: {e}")

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

    def normalize_and_merge(self):
        """
        Normalize column names, add a dataset type column, and merge all datasets into one DataFrame.
        Returns:
            A single merged DataFrame containing all datasets.
        """
        merged_data = []

        # Loop through all dataset types and their respective datasets
        for dataset_type, datasets in self.dataframes_by_type.items():
            for dataset_key, df in datasets.items():
                # Normalize column names (e.g., rename 'DisplayName' to 'UnitName')
                df = df.rename(columns={'DisplayName': 'UnitName'})

                # Add a column specifying the dataset type (e.g., V2, S2, O2)
                df['DatasetType'] = dataset_type

                # Append to the list for merging
                merged_data.append(df)

        # Concatenate all normalized DataFrames into one
        if merged_data:
            self.merged_dataframe = pd.concat(merged_data, ignore_index=True)
            print("All datasets have been normalized and merged successfully.")
        else:
            print("No datasets available to merge.")
            return pd.DataFrame()  # Return an empty DataFrame if no data is available

    def get_merged_dataframe(self):
        """
        Retrieve the merged DataFrame.
        """
        if self.merged_dataframe is None:
            print("Merged DataFrame is not available. Please run normalize_and_merge() first.")
            return pd.DataFrame()  # Return an empty DataFrame if not available
        return self.merged_dataframe