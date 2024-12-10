from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure, Scatter


def register_callbacks(app, merged_dataframe):
    # Line chart callback
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('dataset-type-dropdown', 'value')]
    )
    def update_line_chart(selected_year, dataset_type):
        # Filter data based on dataset type
        df = merged_dataframe[merged_dataframe['DatasetType'] == dataset_type]

        # Ensure required columns are present
        if 'Year' not in df.columns or 'RegularMembers' not in df.columns:
            return px.line(title="Dataset does not have required columns: 'Year' and 'RegularMembers'")

        # Aggregate RegularMembers by year
        df_grouped = df.groupby('Year', as_index=False)['RegularMembers'].sum()

        # Create the line chart
        fig = px.line(
            df_grouped,
            x='Year',
            y='RegularMembers',
            title="Regular Members Over Time",
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

        # Ensure consistent x-axis
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
        Output('hierarchy-treemap', 'figure'),
        [Input('year-slider', 'value')]
    )
    def update_hierarchy_treemap(selected_year):
        # Filter the data based on dataset type and year
        df = merged_dataframe[
            (merged_dataframe['Year'] == selected_year)
            ].copy()  # Work on a copy to avoid modifying the original DataFrame

        # Ensure required columns are present
        if 'RegistrationNumber' not in df.columns or 'UnitName' not in df.columns or 'Members' not in df.columns:
            return px.treemap(title="Dataset does not have required columns: 'RegistrationNumber', 'UnitName', and 'Members'")

        # Split RegistrationNumber into hierarchy levels safely
        df['Level1'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[0] if len(x) > 0 else None)
        df['Level2'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[1] if len(x) > 1 else None)
        df['Level3'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[2] if len(x) > 2 else None)
        print(df.head())
        print(df.columns.tolist())

        # Replace NaN with an empty string for levels without children
        df.fillna('', inplace=True)

        # Create the treemap
        fig = px.treemap(
            df,
            path=['Level1', 'Level2', 'Level3', 'UnitName'],  # Define hierarchy levels
            values='Members',                                # Use 'Members' as the size of rectangles
            title=f"Hierarchy Treemap for year {selected_year}",
            labels={'Members': 'Number of Members'}
        )
        return fig