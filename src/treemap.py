# Initialize DataLoader
from src.DataLoader import DataLoader
from src.utils import add_hierarchy_levels
import plotly.express as px


data_directory = '../data'
data_loader = DataLoader(data_directory)
dataframes = data_loader.load_all_csvs()  # Load datasets
data_loader.normalize_and_merge()
merged_dataframe = data_loader.get_merged_dataframe()
merged_dataframe = add_hierarchy_levels(merged_dataframe)

hierarchy_levels = ['LevelKraj', 'LevelOkres', 'LevelStredisko', 'LevelOddil', 'LevelDruzina']
value_column = "RegularMembers"

merged_dataframe = merged_dataframe.dropna(subset=['RegularMembers'])  # Drop NaN values
merged_dataframe = merged_dataframe[merged_dataframe['RegularMembers'] > 0]  # Drop zero values

if 'UnitName' not in merged_dataframe.columns:
    raise ValueError("Column 'UnitName' not found in the dataset")

# Create the treemap
fig = px.treemap(
    merged_dataframe,
    path=hierarchy_levels,  # Hierarchy levels
    values=value_column,    # Size of nodes
    title="Hierarchical Treemap",
    custom_data=['UnitName']  # Pass the 'UnitName' column for hover customization
)

# Customize hover template to display UnitName
fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>Members: %{value}<extra></extra>"
)


# Show the treemap
fig.show()