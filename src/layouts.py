# layouts.py
from dash import dcc, html

def create_layout(dataset_names):
    return html.Div([
        html.H1("Scouts Over the Years", style={'textAlign': 'center'}),

        # Dropdown for selecting datasets
        html.Label("Select Dataset:"),
        dcc.Dropdown(
            id='dataset-dropdown',
            options=[{'label': name, 'value': name} for name in dataset_names],
            value=dataset_names[0] if dataset_names else None,  # Default to first dataset
        ),

        # Line chart
        dcc.Graph(id='line-chart'),

        # Slider for filtering years
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id='year-slider',
            min=2016,
            max=2024,
            step=1,
            marks={year: str(year) for year in range(2016, 2025)},
            value=[2016, 2024]
        ),
    ])
