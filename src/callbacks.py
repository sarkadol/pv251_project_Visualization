from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure, Scatter


def register_callbacks(app, merged_dataframe):
    # Line chart callback
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('level0-dropdown', 'value')]
    )
    def update_line_chart(selected_year, level0_value):
        # Start with the full dataset
        df = merged_dataframe.copy()

        # Debug print
        print(f"Selected year: {selected_year}")
        print(f"Selected Level0: {level0_value}")

        # Further filter data based on Level0 if a value is selected
        if level0_value and level0_value != 'ALL':
            df = df[df['RegistrationNumber'].str[:2] == level0_value[:2]]  # Correct filtering

        # Ensure required columns are present
        #if 'Year' not in df.columns or 'RegularMembers' not in df.columns:
        #    return px.line(title="Dataset does not have required columns: 'Year' and 'RegularMembers'")

        # Aggregate RegularMembers by year
        df_grouped = df.groupby('Year', as_index=False)['RegularMembers'].sum()


        # Determine the dynamic title
        if level0_value == 'ALL' or not level0_value:
            title = "Regular Members Over Time (All Regions)"
        else:
            title = f"Regular Members Over Time ({level0_value})"  # Fallback to raw value if no match


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
         Input('dataset-type-dropdown', 'value')]
    )
    def update_bar_chart(selected_year, dataset_type):
        # Filter data based on dataset type and year
        df = merged_dataframe[
            (merged_dataframe['DatasetType'] == dataset_type) &
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
