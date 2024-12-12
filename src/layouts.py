from dash import dcc, html

def create_layout(merged_dataframe):
    return html.Div(
        className="main-container",
        children=[
            html.H1("Scouts Data Visualization"),

            html.Div(
                className="dropdown-container",
                children=[
                    html.Label("Select Dataset Type:"),
                    dcc.Dropdown(
                        id='dataset-type-dropdown',
                        options=[
                            {'label': 'Oddily (O2)', 'value': 'O2'},
                            {'label': 'Strediska (S2)', 'value': 'S2'},
                            {'label': 'Okres/Kraj (V2)', 'value': 'V2'}
                        ],
                        value='V2',
                        className="dropdown"
                    ),
                    html.Label("Select Level0 Region:"),
                    dcc.Dropdown(
                        id='level0-dropdown',
                        options=[
                            {'label': level0, 'value': level0} for level0 in merged_dataframe['Level0'].unique()
                        ],
                        placeholder="Select a Level0 region",
                        multi=False,
                        clearable=True
                    ),
                ]
            ),

            html.Div(
                className="chart-container",
                children=[
                    html.Label("Total Over the Years:"),
                    dcc.Loading(
                        id="loading-line-chart",
                        type="circle",
                        children=[dcc.Graph(id='line-chart', className="graph")]
                    )
                ]
            ),

            html.Div(
                className="slider-container",
                children=[
                    html.Label("Select Year:"),
                    dcc.Slider(
                        id='year-slider',
                        min=2016,
                        max=2024,
                        step=1,
                        marks={year: str(year) for year in range(2016, 2025)},
                        value=2024,
                        included=False,
                        tooltip={"placement": "bottom", "always_visible": True},
                        className="slider"
                    )
                ]
            ),

            html.Div(
                className="chart-container",
                children=[
                    html.Label("Age Group Distribution:"),
                    dcc.Loading(
                        id="loading-age-group-bar-chart",
                        type="circle",
                        children=[dcc.Graph(id='age-group-bar-chart', className="graph")]
                    )
                ]
            ),

            html.Hr(),

            html.Div(
                className="chart-container",
                children=[
                    html.H3("Hierarchy - Treemap"),
                    dcc.Loading(
                        id="loading-hierarchy-treemap",
                        type="circle",
                        children=[dcc.Graph(id='hierarchy-treemap', className="graph")]
                    )
                ]
            )
        ]
    )
