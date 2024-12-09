from dash import Dash
from DataLoader import DataLoader
from layouts import create_layout
from callbacks import register_callbacks

# Initialize DataLoader
data_directory = '../data'
data_loader = DataLoader(data_directory)
dataframes = data_loader.load_all_csvs()  # Load datasets

# Extract dataset names
dataset_names = list(dataframes.keys())

# Data types preview
#data_loader.get_preview()
#data_loader.get_preview(dataset_type='V2')
#print("get merged dataframe:")
#print(data_loader.get_merged_dataframe('V2'))

# Initialize Dash app
app = Dash(__name__)
app.layout = create_layout()  # Pass dataset names to the layout

# Register callbacks
register_callbacks(app, data_loader)  # Register the callbacks and pass the DataLoader instance

if __name__ == '__main__':
    app.run_server(debug=True)
