# callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from src.utils import create_hierarchy_tree


def register_callbacks(app, data_loader):
    # Callback for line chart (already provided)
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('dataset-type-dropdown', 'value')]
    )
    def update_line_chart(selected_year, dataset_type):
        # Access the merged dataset
        df = data_loader.get_merged_dataframe(dataset_type)

        # Ensure the required columns are present
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
        # Add a scatter trace to highlight the selected year
        if selected_year in df_grouped['Year'].values:
            selected_year_value = df_grouped[df_grouped['Year'] == selected_year]['RegularMembers'].iloc[0]
            fig.add_scatter(
                x=[selected_year],
                y=[selected_year_value],
                mode='markers',
                marker=dict(size=12, color='red', symbol='circle'),
                #name=f'Selected Year: {selected_year}'
            )

        # Customize the layout to ensure consistent X-axis
        fig.update_traces(line=dict(width=3))  # Thicker line for better visibility
        fig.update_layout(
            xaxis=dict(dtick=1),  # Ensure all years are shown on the X-axis
            yaxis=dict(title="Regular Members"),
            title_x=0.5  # Center the chart title
        )
        return fig

    # New callback for the bar chart
    @app.callback(
        Output('age-group-bar-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('dataset-type-dropdown', 'value')]
    )
    def update_bar_chart(selected_year, dataset_type):
        # Access the merged dataset
        df = data_loader.get_merged_dataframe(dataset_type)

        # Ensure the required columns are present
        required_columns = [
            'Year', 'MembersTo6', 'MembersTo15', 'MembersTo18', 'MembersTo26', 'MembersFrom26'
        ]
        if not all(col in df.columns for col in required_columns):
            return px.bar(title="Dataset does not have required columns for age groups.")

        # Filter data for the selected year
        df_filtered = df[df['Year'] == selected_year]

        # Aggregate data for age groups
        age_groups = {
            '0-6': df_filtered['MembersTo6'].sum(),
            '7-15': df_filtered['MembersTo15'].sum(),
            '16-18': df_filtered['MembersTo18'].sum(),
            '19-26': df_filtered['MembersTo26'].sum(),
            '27+': df_filtered['MembersFrom26'].sum()
        }

        # Convert the aggregated data into a DataFrame for plotting
        age_group_df = pd.DataFrame({
            'AgeGroup': age_groups.keys(),
            'Members': age_groups.values()
        })

        # Create the bar chart
        fig = px.bar(
            age_group_df,
            x='AgeGroup',
            y='Members',
            title=f"Age Group Distribution in {selected_year}",
            labels={'AgeGroup': 'Age Group', 'Members': 'Number of Members'},
            text_auto=True  # Add value labels on bars
        )
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Number of Members",
            title_x=0.5,  # Center the chart title
            barmode='group'
        )
        return fig
    # Tree Diagram
    @app.callback(
        Output('hierarchy-tree', 'figure'),
        [Input('year-slider', 'value')]
    )
    def update_hierarchy_tree(selected_year):
        # Load datasets
        v2_df = data_loader.get_merged_dataframe('V2')
        s2_df = data_loader.get_merged_dataframe('S2')
        o2_df = data_loader.get_merged_dataframe('O2')

        # Generate the hierarchy tree
        return create_hierarchy_tree(v2_df, s2_df, o2_df, selected_year)



    # Sunburst Chart
    @app.callback(
        Output('hierarchy-sunburst', 'figure'),
        Input('dataset-type-dropdown', 'value')
    )
    def update_sunburst(dataset_type):
        df = data_loader.get_merged_dataframe(dataset_type)

        if 'RegistrationNumber' not in df.columns or 'UnitName' not in df.columns:
            return px.line(title="Dataset does not have required columns: 'RegistrationNumber' and 'UnitName'")

        df['Hierarchy'] = df['RegistrationNumber'].str.split('.')

        sunburst_data = []
        for _, row in df.iterrows():
            levels = row['Hierarchy']
            for i in range(1, len(levels) + 1):
                sunburst_data.append({
                    'ID': '.'.join(levels[:i]),
                    'Parent': '.'.join(levels[:i - 1]) if i > 1 else '',
                    'Name': row['UnitName'] if i == len(levels) else ''
                })

        sunburst_df = pd.DataFrame(sunburst_data)
        return px.sunburst(sunburst_df, path=['Parent', 'ID'], hover_name='Name', title="Hierarchy Sunburst Chart")

    # Dropdown Filtering
    @app.callback(
        [Output('parent-dropdown', 'options'), Output('parent-dropdown', 'value')],
        Input('dataset-type-dropdown', 'value')
    )
    def update_dropdown(dataset_type):
        df = data_loader.get_merged_dataframe(dataset_type)
        parent_units = df['RegistrationNumber'].unique()
        options = [{'label': unit, 'value': unit} for unit in parent_units]
        return options, options[0]['value'] if options else None

    @app.callback(
        Output('hierarchy-graph', 'figure'),
        [Input('parent-dropdown', 'value'), Input('dataset-type-dropdown', 'value')]
    )
    def update_hierarchy_graph(selected_parent, dataset_type):
        df = data_loader.get_merged_dataframe(dataset_type)

        if 'RegistrationNumber' not in df.columns or 'UnitName' not in df.columns or 'Members' not in df.columns:
            return px.line(title="Dataset does not have required columns: 'RegistrationNumber', 'UnitName', 'Members'")

        filtered_df = df[df['RegistrationNumber'].str.startswith(selected_parent)]
        return px.bar(filtered_df, x='UnitName', y='Members', title=f"Units under {selected_parent}")

    # Table Display
    @app.callback(
        Output('hierarchy-table', 'data'),
        Input('dataset-type-dropdown', 'value')
    )
    def update_table(dataset_type):
        df = data_loader.get_merged_dataframe(dataset_type)
        return df.to_dict('records')



