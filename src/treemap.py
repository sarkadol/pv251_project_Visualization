# Initialize DataLoader

from src.DataLoader import DataLoader
from src.utils import add_hierarchy_levels,add_hierarchy_levels_whole
import plotly.express as px


data_directory = '../data'
data_loader = DataLoader(data_directory)
dataframes = data_loader.load_all_csvs()  # Load datasets
data_loader.normalize_and_merge()
df = data_loader.get_merged_dataframe()
df = add_hierarchy_levels(df)
df = add_hierarchy_levels_whole(df)

hierarchy_levels = [px.Constant("all"),'LevelKrajWhole', 'LevelOkresWhole', 'LevelStrediskoWhole', 'LevelOddilWhole', 'LevelDruzinaWhole']
value_column = "RegularMembers"

df = df.dropna(subset=['RegularMembers'])  # Drop NaN values
df = df[df['RegularMembers'] > 0]  # Drop zero values
#print(merged_dataframe.to_string())
#print(merged_dataframe['UnitName'])
df = df[df['Year'] == 2024]
df = df[~df['ID_UnitType'].isin(['ustredi', 'zvlastniJednotka'])]

if 'UnitName' not in df.columns:
    raise ValueError("Column 'UnitName' not found in the dataset")
# Define the color palette with 14 colors
# Define the color palette with 14 colors
logo_palette = [
    "#D4B66D", "#B85637", "#A21F16", "#732813", "#5D4716",
    "#8D5F0F", "#48651D", "#5C748C"
]

# Create the treemap
fig = px.treemap(
    df,
    path=hierarchy_levels,  # Hierarchy levels
    values=value_column,    # Size of nodes
    title="Hierarchical Treemap",
    labels=df['UnitName'],  # Custom
    custom_data=[df['UnitName']],  # Custom
    color_discrete_sequence=logo_palette  # Apply the custom color palette
)

# Customize hover template and texttemplate
fig.update_traces(
    root_color="lightgrey",
    hovertemplate="<b>%{customdata[0]}</b><br>"
                  "Members: %{value}<br>"
                  "<extra></extra>",
    text=df['UnitName'],
    texttemplate="<b>%{customdata[0]}</b><br>",
    marker=dict(cornerradius=5)
)

# Show the treemap
fig.show()
