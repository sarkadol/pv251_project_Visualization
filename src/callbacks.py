# callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px

def register_callbacks(app, data_loader):
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('dataset-dropdown', 'value'),
         Input('year-slider', 'value')]
    )
    def update_line_chart(dataset_name, year_range):
        # Validate dataset selection
        if not dataset_name or dataset_name not in data_loader.dataframes:
            return px.line(title="No dataset selected or dataset not found")

        # Get the selected dataset
        df = data_loader.dataframes[dataset_name]

        # Ensure the required columns are present
        if 'Year' not in df.columns or 'RegularMembers' not in df.columns:
            return px.line(title="Dataset does not have required columns: 'Year' and 'RegularMembers'")

        # Filter data based on the selected year range
        df_filtered = df[(df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1])]

        # Aggregate RegularMembers by year
        df_grouped = df_filtered.groupby('Year', as_index=False)['RegularMembers'].sum()

        # Create the line chart
        fig = px.line(
            df_grouped,
            x='Year',
            y='RegularMembers',
            title=f"Regular Members Over Time ({year_range[0]}-{year_range[1]})",
            labels={'Year': 'Year', 'RegularMembers': 'Regular Members'}
        )
        return fig
