from dash import dcc, html

def create_layout(merged_dataframe):
    return html.Div(
        className="main-container",
        children=[
            html.H1("Scouts Data Visualization"),
            # Main Container for Line Chart and Information Section
            html.Div(
                className="container",
                style={"display": "flex", "flexDirection": "row", "alignItems": "stretch"},
                children=[
                    # Left Section: Line Chart and Slider
                    html.Div(
                        className="left-section",
                        children=[
                            # Line Chart
                            dcc.Loading(
                                id="loading-line-chart",
                                type="circle",
                                children=[
                                    dcc.Graph(
                                        id='line-chart',
                                        className="line-chart",
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
                            ),
                            # Year Slider
                            html.Div(
                                className="slider-container",
                                children=[
                                    dcc.Slider(
                                        id='year-slider',
                                        min=2016,
                                        max=2024,
                                        step=1,
                                        marks={year: str(year) for year in range(2016, 2025)},
                                        value=2024,
                                        included=False,
                                        tooltip={"placement": "bottom", "always_visible": True}
                                    )
                                ]
                            )
                        ]
                    ),
                    # Right Section: About the Project
                    html.Div(
                        className="right-section",
                        children=[
                            html.H2("About the Project"),
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
                        ]
                    )
                ]
            ),
            # Dropdowns
            html.Div(
                className="dropdown-container",
                children=[
                    html.Label("Select Level0 Region:"),
                    dcc.Dropdown(
                        id='level0-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "kraj"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL'
                    ),
                    html.Label("Select Level1 (Okres):"),
                    dcc.Dropdown(
                        id='level1-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "okres"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL'
                    ),
                    html.Label("Select Level2 (Stredisko):"),
                    dcc.Dropdown(
                        id='level2-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "stredisko"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL'
                    ),
                    html.Label("Select Level3 (Oddíl):"),
                    dcc.Dropdown(
                        id='level3-dropdown',
                        options=[
                                    {'label': 'ALL', 'value': 'ALL'}
                                ] + [
                                    {'label': unit_name, 'value': registration_number}
                                    for registration_number, unit_name in merged_dataframe[
                                merged_dataframe['ID_UnitType'] == "oddil"
                                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
                                ],
                        value='ALL'
                    )
                ]
            ),
            # Bar Chart Section
            html.Div(
                className="bar-chart-section",
                children=[
                    dcc.Loading(
                        id="loading-age-group-bar-chart",
                        type="circle",
                        children=[dcc.Graph(id='age-group-bar-chart')]
                    )
                ]
            ),
            # Treemap Section
            html.Hr(),
            html.Div(id="treemap-trigger"),
            html.Div(
                className="treemap-section",
                children=[
                    html.H3("Hierarchy - Treemap"),
                    dcc.Loading(
                        id="loading-hierarchy-treemap",
                        type="circle",
                        children=[
                            dcc.Graph(id='hierarchy-treemap')
                        ]
                    )
                ]
            )
        ]
    )
