from dash import Dash
from DataLoader import DataLoader
from layouts import create_layout
from callbacks import register_callbacks
from utils import add_hierarchy_levels,add_hierarchy_levels_whole,add_hierarchy_levels_text

# Initialize DataLoader
data_directory = '../data'
data_loader = DataLoader(data_directory)
if(True):
    # use one already merged file
    data_loader.load_merged_dataframe('./src/merged_dataframe.csv')
else:
    # load a new csv or play with encoding
    dataframes = data_loader.load_all_csvs()  # Load datasets
    data_loader.normalize_and_merge()

merged_dataframe = data_loader.get_merged_dataframe()
merged_dataframe = add_hierarchy_levels(merged_dataframe)
#merged_dataframe = add_hierarchy_levels_whole(merged_dataframe) #needed for treemap


merged_dataframe = add_hierarchy_levels_text(merged_dataframe) #needed for treemap

# Initialize Dash app
app = Dash(__name__, assets_folder='assets')
app.layout = create_layout(merged_dataframe)  # Pass dataset names to the layout

if __name__ == '__main__':
    register_callbacks(app, merged_dataframe)
    app.run_server(debug=True)
