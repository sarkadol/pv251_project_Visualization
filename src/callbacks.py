from dash import no_update
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

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
        print(f"Selected year: {selected_year}")
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

        # Ensure consistent x-axis and y-axis range
        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            xaxis=dict(dtick=1),
            yaxis=dict(title="Regular Members"),
            title_x=0.5
        )
        return fig
    # Bar chart for age groups callback
    @app.callback(
        Output('age-group-bar-chart', 'figure'),
        [Input('year-slider', 'value'),
         ]
    )
    def update_bar_chart(selected_year):
        # Filter data based on dataset type and year
        df = merged_dataframe[
            (merged_dataframe['Year'] == selected_year)
            ]

        # Ensure required columns are present
        required_columns = ['MembersTo6', 'MembersTo15', 'MembersTo18', 'MembersTo26', 'MembersFrom26']
        if not all(col in df.columns for col in required_columns):
            """
    if level0_value and level0_value != 'ALL':
        # Filter Level1 options based on Level0
        level1_options += [
            {'label': unit_name, 'value': registration_number}
            for registration_number, unit_name in df[
                df['RegistrationNumber'].str.startswith(level0_value) & (df['ID_UnitType'] == "okres")
                ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
        ]

    # Filter Level2 options based on Level0
    level2_options += [
        {'label': unit_name, 'value': registration_number}
        for registration_number, unit_name in df[
            df['RegistrationNumber'].str.startswith(level0_value) & (df['ID_UnitType'] == "stredisko")
            ][['RegistrationNumber', 'UnitName']].drop_duplicates().values
    ]
        @app.callback(
            Output('hierarchy-treemap', 'figure'),
            [Input('year-slider', 'value')]
        )
        def update_hierarchy_treemap(selected_year):
            pass"""
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

        # Create the bar chart
        fig = px.bar(
            age_group_df,
            x='AgeGroup',
            y='Members',
            title=f"Age Group Distribution in {selected_year}",
            labels={'AgeGroup': 'Age Group', 'Members': 'Number of Members'},
            text_auto=True
        )
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Number of Members",
            title_x=0.5,
            barmode='group'
        )
        return fig

    @app.callback(
        [
            Output('level1-dropdown', 'options'),
            Output('level2-dropdown', 'options'),
            Output('level3-dropdown', 'options'),
            Output('level1-dropdown', 'value'),
            Output('level2-dropdown', 'value'),
            Output('level3-dropdown', 'value'),
        ],
        [
            Input('level0-dropdown', 'value')
        ]
    )
    def update_from_level0(level0_value):
        # Start with the full dataset
        df = merged_dataframe.copy()

        # Debug prints for Level0 value
        print(f"Selected Level0: {level0_value}")

        # Default options for Level1, Level2, and Level3
        level1_options = [{'label': 'ALL', 'value': 'ALL'}]
        level2_options = [{'label': 'ALL', 'value': 'ALL'}]
        level3_options = [{'label': 'ALL', 'value': 'ALL'}]

        if level0_value and level0_value != 'ALL':
            # Match first two characters of RegistrationNumber
            first_two_digits = level0_value[:2]
            print(f"Filtering for first two digits: {first_two_digits}")

            # Filter Level1 using the first two characters of RegistrationNumber
            filtered_level1 = df[
                (df['RegistrationNumber'].str[:2] == first_two_digits) & (df['ID_UnitType'] == "okres")
                ]
            #print(f"Filtered Level1 options:\n{filtered_level1}")
            level1_options += [
                {'label': unit_name, 'value': registration_number}
                for registration_number, unit_name in filtered_level1[['RegistrationNumber', 'UnitName']].drop_duplicates().values
            ]

            # Filter Level2 using the first two characters of RegistrationNumber
            filtered_level2 = df[
                (df['RegistrationNumber'].str[:2] == first_two_digits) & (df['ID_UnitType'] == "stredisko")
                ]
            #print(f"Filtered Level2 options:\n{filtered_level2}")
            level2_options += [
                {'label': unit_name, 'value': registration_number}
                for registration_number, unit_name in filtered_level2[['RegistrationNumber', 'UnitName']].drop_duplicates().values
            ]

            # Filter Level3 using the first two characters of RegistrationNumber
            filtered_level3 = df[
                (df['RegistrationNumber'].str[:2] == first_two_digits) & (df['ID_UnitType'] == "oddil")
                ]
            #print(f"Filtered Level3 options:\n{filtered_level3}")
            level3_options += [
                {'label': unit_name, 'value': registration_number}
                for registration_number, unit_name in filtered_level3[['RegistrationNumber', 'UnitName']].drop_duplicates().values
            ]

        # If "ALL" is selected, reset all values to "ALL"
        return level1_options, level2_options, level3_options, 'ALL', 'ALL', 'ALL'

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

