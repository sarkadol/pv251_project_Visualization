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
                            {'label': unit_name, 'value': level0}
                            for level0, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "kraj"  # Filter rows where ID_UnitType equals "kraj"
                                ][['Level0', 'UnitName']].drop_duplicates().values
                        ],
                        placeholder="Select a Level0 region",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level1 (Okres):"),
                    dcc.Dropdown(
                        id='level1-dropdown',
                        options=[
                            {'label': unit_name, 'value': level1}
                            for level1, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "okres"  # Filter rows where ID_UnitType equals "okres"
                                ][['Level1', 'UnitName']].drop_duplicates().values
                        ],
                        placeholder="Select a Level1 (Okres)",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level2 (Stredisko):"),
                    dcc.Dropdown(
                        id='level2-dropdown',
                        options=[
                            {'label': unit_name, 'value': level2}
                            for level2, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "stredisko"  # Filter rows where ID_UnitType equals "stredisko"
                                ][['Level2', 'UnitName']].drop_duplicates().values
                        ],
                        placeholder="Select a Level2 (Stredisko)",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level3 (Oddíl):"),
                    dcc.Dropdown(
                        id='level3-dropdown',
                        options=[
                            {'label': unit_name, 'value': level3}
                            for level3, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "oddil"  # Filter rows where ID_UnitType equals "oddíl"
                                ][['Level3', 'UnitName']].drop_duplicates().values
                        ],
                        placeholder="Select a Level3 (Oddíl)",
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
