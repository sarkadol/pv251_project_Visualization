from dash import no_update
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

pestra_palette = [
    "#FFCC00", "#EE8027", "#E53434", "#A0067D", "#5E2281",
    "#172983", "#007BC2", "#89BA17"
]

logo_palette = [
    "#FCC11E", "#F9B200", "#F49E00", "#294885", "#255C9E",
    "#336CAA", "#3979B5"
]

def register_callbacks(app, merged_dataframe):
    # Line chart callback
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('level0-dropdown', 'value'),
         Input('level1-dropdown', 'value'),
         Input('level2-dropdown', 'value'),
         Input('level3-dropdown', 'value')])
    def update_line_chart(selected_year, level0_value, level1_value, level2_value, level3_value):
        # Start with the full dataset
        df = merged_dataframe.copy()

        # Debug print
        #print(f"Selected year: {selected_year}")
        print(f"Level0: {level0_value}, Level1: {level1_value}, Level2: {level2_value}, Level3: {level3_value}")

        # Determine the most specific level to use
        selected_level = None
        selected_value = None

        if level3_value != 'ALL':
            selected_level = 'oddil'
            selected_value = level3_value
        elif level2_value != 'ALL':
            selected_level = 'stredisko'
            selected_value = level2_value
        elif level1_value != 'ALL':
            selected_level = 'okres'
            selected_value = level1_value
        elif level0_value != 'ALL':
            selected_level = 'kraj'
            selected_value = level0_value

        # Filter the dataset if a specific level is selected
        if selected_value:
            df = df[df['RegistrationNumber'] == selected_value]

        # Retrieve the UnitName for the title
        unit_name = None
        if selected_value:
            unit_row = df[df['RegistrationNumber'] == selected_value]
            if not unit_row.empty:
                unit_name = unit_row['UnitName'].iloc[0]

        # Aggregate RegularMembers by year
        df_grouped = df.groupby('Year', as_index=False)['RegularMembers'].sum()

        # Determine the dynamic title
        if level0_value == 'ALL' or not level0_value:
            title = "Regular Members Over Time (All Regions)"
        else:
            title = f"Regular Members Over Time ({unit_name})" if unit_name else f"Regular Members Over Time ({level0_value})"


        # Create the line chart
        fig = px.line(
            df_grouped,
            x='Year',
            y='RegularMembers',
            title=title,
            labels={'Year': 'Year', 'RegularMembers': 'Regular Members'}
        )

        # Highlight the selected year
        if selected_year in df_grouped['Year'].values:
            selected_year_value = df_grouped[df_grouped['Year'] == selected_year]['RegularMembers'].iloc[0]
            fig.add_scatter(
                x=[selected_year],
                y=[selected_year_value],
                mode='markers',
                marker=dict(size=12, color='red', symbol='circle')
            )
        y_max = df_grouped['RegularMembers'].max() * 1.2 if not df_grouped.empty else 10  # Add 10% padding or use a default


    # Ensure consistent x-axis and y-axis range
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            xaxis=dict(dtick=1),
            yaxis=dict(title="# regular members",range=[0, y_max]),
            title_x=0.5,
            showlegend=False,
            transition_duration=2000,  # Smooth animation duration
        )


        return fig
    # Bar chart for age groups callback
    @app.callback(
        Output('age-group-bar-chart', 'figure'),
        [
            Input('year-slider', 'value'),
            Input('level0-dropdown', 'value'),
            Input('level1-dropdown', 'value'),
            Input('level2-dropdown', 'value'),
            Input('level3-dropdown', 'value'),
        ]
    )
    def update_bar_chart(selected_year, level0_value, level1_value, level2_value, level3_value):
        # Start with the full dataset
        df = merged_dataframe.copy()

        # Determine the most specific level to use
        selected_level = None
        selected_value = None

        if level3_value != 'ALL':
            selected_level = 'oddil'
            selected_value = level3_value
        elif level2_value != 'ALL':
            selected_level = 'stredisko'
            selected_value = level2_value
        elif level1_value != 'ALL':
            selected_level = 'okres'
            selected_value = level1_value
        elif level0_value != 'ALL':
            selected_level = 'kraj'
            level0_value_short = level0_value[:2]
            selected_value = level0_value


        # Filter the dataset if a specific level is selected
        if selected_value:
            df = df[df['RegistrationNumber'] == selected_value]

        # Further filter by the selected year
        df = df[df['Year'] == selected_year]

        # Ensure required columns are present
        required_columns = ['MembersTo6', 'MembersTo15', 'MembersTo18', 'MembersTo26', 'MembersFrom26']
        if not all(col in df.columns for col in required_columns):
            return px.bar(title="Dataset does not have required columns for age groups.")

        # Aggregate data for age groups
        age_groups = {
            '0-6': df['MembersTo6'].sum(),
            '7-15': df['MembersTo15'].sum(),
            '16-18': df['MembersTo18'].sum(),
            '19-26': df['MembersTo26'].sum(),
            '27+': df['MembersFrom26'].sum()
        }

        # Create a DataFrame for plotting
        age_group_df = pd.DataFrame({'AgeGroup': age_groups.keys(), 'Members': age_groups.values()})

        # Retrieve the UnitName for the title
        unit_name = None
        if selected_value:
            unit_row = merged_dataframe[merged_dataframe['RegistrationNumber'] == selected_value]
            if not unit_row.empty:
                unit_name = unit_row['UnitName'].iloc[0]

        # Determine the dynamic title
        if level0_value == 'ALL' or not level0_value:
            title = f"Age Group Distribution in {selected_year} (All Regions)"
        else:
            title = f"Age Group Distribution in {selected_year} ({unit_name})" if unit_name else f"Age Group Distribution in {selected_year} ({level0_value})"
        print(title)

        # Create the bar chart
        fig = px.bar(
            age_group_df,
            x='AgeGroup',
            y='Members',
            title=title,
            labels={'AgeGroup': 'Age Group', 'Members': 'Number of Members'},
            text_auto=True,
            color='AgeGroup',
            color_discrete_sequence=pestra_palette
        )

        # Update layout and formatting
        fig.update_layout(
            xaxis_title="Age group",
            yaxis_title="# regular members",
            title_x=0.5,
            showlegend=False,  # Disable the legend
            bargap=0.1,  # Adjust space between bars (set closer to 0 to make bars wider)
            barmode='group',
            #transition_duration=2000,  # Smooth animation duration
            #title=title,
        )

        # Format hover labels and y-axis
        fig.update_traces(
            hovertemplate='<b>Age Group=%{x}</b><br>Number of Members=%{y:,}<extra></extra>',
            texttemplate='%{y:.3s}',  # Show values in abbreviated form (e.g., 200k)
            textposition='outside',  # Place text above bars
            width=0.9  # Adjust the bar width
        )
        #print("fig.layout.title.text",fig.layout.title.text)  # Ensure the title is as expected


        return fig


    @app.callback(
        [
            Output('level1-dropdown', 'options'),
            Output('level2-dropdown', 'options'),
            Output('level3-dropdown', 'options'),
            Output('level1-dropdown', 'value'),
            Output('level2-dropdown', 'value'),
            Output('level3-dropdown', 'value')
        ],
        [
            Input('level0-dropdown', 'value'),
            Input('level1-dropdown', 'value'),
            Input('level2-dropdown', 'value'),
            Input('level3-dropdown', 'value')
        ]
    )
    def update_dropdowns(level0_value, level1_value, level2_value, level3_value):
        # Filter for LevelKraj
        level0_value_short = level0_value[:2]  # Ensure the top-level value is shortened to match
        # level0value for ALL is then AL - solved, made problems in get_options

        # Filters dictionary for cascading filtering
        filters = {'LevelKraj': level0_value_short, 'LevelOkres': level1_value, 'LevelStredisko': level2_value}

        # Update Level 1 (Okres) options based on LevelKraj
        level1_options = get_options(merged_dataframe, current_level='LevelOkres', parent_filters={'LevelKraj': level0_value_short})
        level1_value = level1_value if level1_value in [opt['value'] for opt in level1_options] else 'ALL'

        # Update Level 2 (Stredisko) options based on LevelKraj and LevelOkres
        level2_options = get_options(merged_dataframe, current_level='LevelStredisko', parent_filters={'LevelKraj': level0_value_short, 'LevelOkres': level1_value})
        level2_value = level2_value if level2_value in [opt['value'] for opt in level2_options] else 'ALL'

        # Update Level 3 (Oddil) options based on all parent levels
        level3_options = get_options(merged_dataframe, current_level='LevelOddil', parent_filters=filters)
        level3_value = level3_value if level3_value in [opt['value'] for opt in level3_options] else 'ALL'

        # Debugging output
        #print(f"Level0 Value: {level0_value_short}")
        #print(f"Level1 Value: {level1_value}")
        #print(f"Level2 Value: {level2_value}")
        #print(f"Level3 Value: {level3_value}")

        return level1_options, level2_options, level3_options, level1_value, level2_value, level3_value

    @app.callback(
        Output('hierarchy-treemap', 'figure'),
        Input('loading-hierarchy-treemap', 'children')  # Placeholder trigger
    )
    def generate_dynamic_treemap(_):
        """
        Create a static hierarchy treemap from the DataFrame with renamed hierarchy levels.
        """
        # Validate DataFrame columns
        if 'LevelKraj' not in merged_dataframe.columns or 'RegularMembers' not in merged_dataframe.columns:
            raise ValueError("Merged DataFrame missing required columns: 'LevelKraj' or 'RegularMembers'")

        # Debug DataFrame preview
        print("Merged DataFrame Preview:")
        print(merged_dataframe[['LevelKraj', 'LevelOkres', 'LevelStredisko', 'LevelOddil', 'LevelDruzina',
                                'UnitName', 'RegularMembers']].head())

        # Create the treemap with renamed levels
        fig = px.treemap(
            merged_dataframe,
            path=[px.Constant("All"), 'LevelKraj', 'LevelOkres', 'LevelStredisko', 'LevelOddil', 'LevelDruzina'],
            values='RegularMembers',  # Use 'RegularMembers' column for sizes
            hover_data=['UnitName'],      # UnitName will show in hover tooltips
            custom_data=['UnitName']      # Pass UnitName for custom text
        )

        # Update to show UnitName as text
        fig.update_traces(
            texttemplate='%{customdata}',  # Use UnitName for all labels
            hovertemplate='<b>%{customdata}</b><br>Value: %{value}'
        )

        return fig

    @app.callback(
        [
            Output('level0-dropdown', 'value',allow_duplicate=True),
            Output('level1-dropdown', 'value',allow_duplicate=True),
            Output('level2-dropdown', 'value',allow_duplicate=True),
            Output('level3-dropdown', 'value',allow_duplicate=True)
        ],
        [Input('reset-button', 'n_clicks')],
        prevent_initial_call=True
    )
    def reset_dropdowns(n_clicks):
        # Reset all dropdowns to 'ALL' when the button is clicked
        if n_clicks > 0:
            return 'ALL', 'ALL', 'ALL', 'ALL'
        # Initial values
        return no_update


    # Assuming `merged_dataframe` contains hierarchical data
def get_options(dataframe, current_level, parent_filters):
    """
    Get options for a dropdown based on the current level and all selected parent filters.

    Args:
        dataframe (pd.DataFrame): The dataframe containing the hierarchical data.
        current_level (str): The column representing the current level (e.g., 'Level3').
        parent_filters (dict): A dictionary of parent levels and their selected values.

    Returns:
        list: A list of dictionaries with labels and values for the dropdown.
    """
    # Map current levels to their corresponding ID_UnitType
    level_to_unit_type = {
        'LevelOddil': 'oddil',
        'LevelStredisko': 'stredisko',
        'LevelOkres': 'okres'
    }

    # Determine the valid unit type for the current level
    current_unit_type = level_to_unit_type.get(current_level, None)

    # Filter the dataframe for rows matching the current unit type
    if current_unit_type:
        filtered_dataframe = dataframe[dataframe['ID_UnitType'] == current_unit_type]
    else:
        # If the current level does not map to a specific ID_UnitType, use the full dataframe
        filtered_dataframe = dataframe

    # Apply all parent-level filters
    for parent_level, parent_value in parent_filters.items():
        if parent_value not in ['ALL', 'AL']:
            filtered_dataframe = filtered_dataframe[filtered_dataframe[parent_level] == parent_value]

    # Debugging output
    #print(f"Filtered DataFrame for {current_level}:")
    #print(filtered_dataframe.head())

    # Generate options for the dropdown
    return [{'label': 'ALL', 'value': 'ALL'}] + [
        {'label': name, 'value': id_}
        for id_, name in filtered_dataframe[['RegistrationNumber', 'UnitName']].drop_duplicates().values
    ]
