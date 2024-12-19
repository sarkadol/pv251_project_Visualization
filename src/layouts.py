from dash import dcc, html

def create_layout(merged_dataframe):
    return html.Div(
        className="main-container",
        children=[
            html.H1("Scouts Data Visualization"),
            html.Div(
                className="container",
                style={"display": "flex", "flexDirection": "row", "alignItems": "stretch"},  # Flexbox layout
                children=[
                    # Left section: Line chart and slider
                    html.Div(
                        style={"flex": "2", "display": "flex", "flexDirection": "column"},  # Take more space
                        children=[
                            html.Div(
                                children=[

                                    dcc.Loading(
                                        id="loading-line-chart",
                                        type="circle",
                                        children=[
                                            dcc.Graph(
                                                id='line-chart',
                                                className="graph",
                                                config={"staticPlot": False},
                                                style={"width": "100%"},
                                                figure={
                                                    "layout": {
                                                        "xaxis": {"range": [2016, 2024]},
                                                        "yaxis": {},
                                                        "showlegend": False
                                                    }
                                                }
                                            )
                                        ]
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
                                        className="slider",
                                    )
                                ]
                            )
                        ]
                    ),
                    # Right section: Description (Text replaced with paragraphs)
                    html.Div(
                        style={"flex": "1", "paddingLeft": "20px"},  # Take less space
                        children=[
                            html.Div(
                                children=[
                                    html.H2("About the Project"),  # Section title
                                    html.P(
                                        "This dashboard provides an interactive visualization of scouting data. "
                                        "It allows users to explore trends, compare regions, and analyze age group distributions."
                                    ),
                                    html.P([
                                        "Use the ", html.Strong("interactive controls"), " to select specific years, regions, and datasets. "
                                                                                         "The visualizations include line charts, bar charts, and a treemap hierarchy for detailed insights."
                                    ]),
                                    html.P(
                                        "Scroll down to explore the hierarchical treemap, which shows the breakdown of participants "
                                        "by organizational units, such as regions, districts, and groups."
                                    )
                                ],
                                style={
                                    "width": "100%",
                                    "height": "100%",  # Ensures it matches the parent's height
                                    "overflowY": "auto",  # Adds scroll if content overflows
                                    "padding": "10px",  # Adds internal spacing
                                    "backgroundColor": "#f9f9f9",  # Optional: Light background for the section
                                    "border": "1px solid #ccc",  # Optional: Subtle border for clarity
                                    "borderRadius": "5px"  # Optional: Rounded corners
                                }
                            )
                        ]
                    )

                ]
            ),

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
                                    {'label': 'ALL', 'value': 'ALL'}  # Add the "ALL" option here
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "kraj"  # Filter rows where ID_UnitType equals "kraj"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL',
                        placeholder="Select a Level0 region",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level1 (Okres):"),
                    dcc.Dropdown(
                        id='level1-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}  # Add the "ALL" option here
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "okres"  # Filter rows where ID_UnitType equals "okres"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL',
                        placeholder="Select a Level1 (Okres)",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level2 (Stredisko):"),
                    dcc.Dropdown(
                        id='level2-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}  # Add the "ALL" option here
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "stredisko"  # Filter rows where ID_UnitType equals "stredisko"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL',
                        placeholder="Select a Level2 (Stredisko)",
                        multi=False,
                        clearable=True
                    ),

                    html.Label("Select Level3 (Oddíl):"),
                    dcc.Dropdown(
                        id='level3-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}  # Add the "ALL" option here
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "oddil"  # Filter rows where ID_UnitType equals "oddíl"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL',
                        placeholder="Select a Level3 (Oddíl)",
                        multi=False,
                        clearable=True
                    ),

                ],
                style={"width": "28%", "display": "inline-block", "verticalAlign": "top"}
            ),

            html.Div(
                children=[
                    dcc.Loading(
                        id="loading-age-group-bar-chart",
                        type="circle",
                        children=[dcc.Graph(id='age-group-bar-chart', className="graph")]
                    )
                ],
                style={"width": "70%", "display": "inline-block", "verticalAlign": "top"}
            ),



            html.Hr(),
            html.Div(id="treemap-trigger"),  # This serves as the Input

            html.Div(
                children=[
                    html.H3("Hierarchy - Treemap"),
                    dcc.Loading(
                        id="loading-hierarchy-treemap",
                        type="circle",
                        children=[
                            dcc.Graph(id='hierarchy-treemap', className="graph")
                        ]
                    )
                ]
            )
        ]
    )
