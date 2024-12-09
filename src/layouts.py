from dash import dcc, html

def create_layout():
    return html.Div([
        html.H1("Scouts Data Visualization", style={'textAlign': 'center'}),

        # Dropdown to select dataset type
        html.Label("Select Dataset Type:"),
        dcc.Dropdown(
            id='dataset-type-dropdown',
            options=[
                {'label': 'Oddily (O2)', 'value': 'O2'},
                {'label': 'Strediska (S2)', 'value': 'S2'},
                {'label': 'Okres/Kraj (V2)', 'value': 'V2'}
            ],
            value='V2',  # Default to 'V2' because other still have mistakes
        ),

        # Line chart
        dcc.Graph(id='line-chart'),

        # Slider for filtering years
        html.Label("Select Year:"),
        dcc.Slider(
            id='year-slider',
            min=2016,
            max=2024,
            step=1,
            marks={year: str(year) for year in range(2016, 2025)},
            value=2024,  # Default value
            included=False
        ),
        # Bar chart for age groups
        dcc.Graph(id='age-group-bar-chart'),
    ])