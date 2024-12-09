# callbacks.py
from dash.dependencies import Input, Output
import plotly.express as px

def register_callbacks(app, data_loader):
    @app.callback(
        Output('line-chart', 'figure'),
        [Input('year-slider', 'value'),
         Input('dataset-type-dropdown', 'value')]
    )
    def update_line_chart(year_range,dataset_type):
        # Access the merged V2 DataFrame
        df = data_loader.get_merged_dataframe(dataset_type)

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
        fig.update_xaxes(dtick=1)
        return fig

    @app.callback(
        Output('dataset-dropdown', 'options'),
        [Input('dataset-type-dropdown', 'value')]
    )
    def update_dataset_dropdown(dataset_type):
        if dataset_type not in data_loader.dataframes_by_type:
            return []
        return [{'label': key, 'value': key} for key in data_loader.dataframes_by_type[dataset_type].keys()]