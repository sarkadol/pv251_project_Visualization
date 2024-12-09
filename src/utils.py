import pandas as pd
import plotly.express as px

def create_hierarchy_tree(v2_df, s2_df, o2_df, selected_year):
    # Step 1: Filter datasets for the selected year
    v2_filtered = v2_df[v2_df['Year'] == selected_year]
    s2_filtered = s2_df[s2_df['Year'] == selected_year]
    o2_filtered = o2_df[o2_df['Year'] == selected_year]

    # Step 2: Initialize tree data
    tree_data = []

    # Step 3: Add Level 1 (Kraj/Ústředí) from V2
    for _, row in v2_filtered[v2_filtered['RegistrationNumber'].str.match(r'^\d{3}$')].iterrows():
        tree_data.append({
            'ID': row['RegistrationNumber'],  # e.g., 110
            'Parent': '',  # Root nodes have no parent
            'Name': row['UnitName'],  # Name of the unit
            'Level': 1,
            'Size': row['Members']  # Total members as size
        })

    # Step 4: Add Level 2 (Okres) from V2
    for _, row in v2_filtered[v2_filtered['RegistrationNumber'].str.match(r'^\d{3}$') == False].iterrows():
        parent_id = row['RegistrationNumber'][:3]  # Parent is the first 3 digits (e.g., 110)
        tree_data.append({
            'ID': row['RegistrationNumber'],  # e.g., 112
            'Parent': parent_id,  # Parent is Level 1 (e.g., 110)
            'Name': row['UnitName'],  # Name of the unit
            'Level': 2,
            'Size': row['Members']  # Total members as size
        })

    # Step 5: Add Level 3 (Středisko/Zvláštní jednotka) from S2
    for _, row in s2_filtered.iterrows():
        parent_id = row['RegistrationNumber'][:3]  # Parent is Level 2 (e.g., 112)
        tree_data.append({
            'ID': row['RegistrationNumber'],  # e.g., 112.02
            'Parent': parent_id,  # Parent is Level 2
            'Name': row['DisplayName'],  # Name of the unit
            'Level': 3,
            'Size': row['Members']  # Total members as size
        })

    # Step 6: Add Level 4 (Oddíl) from O2
    for _, row in o2_filtered.iterrows():
        parent_id = row['RegistrationNumber'][:6]  # Parent is Level 3 (e.g., 112.02)
        tree_data.append({
            'ID': row['RegistrationNumber'],  # e.g., 112.02.002
            'Parent': parent_id,  # Parent is Level 3
            'Name': row['UnitName'],  # Name of the unit
            'Level': 4,
            'Size': row['Members']  # Total members as size
        })

    # Step 7: Add Optional Level 5 from O2
    for _, row in o2_filtered[o2_filtered['RegistrationNumber'].str.contains('-')].iterrows():
        parent_id = row['RegistrationNumber'].split('-')[0]  # Parent is Level 4 (e.g., 112.02.002)
        tree_data.append({
            'ID': row['RegistrationNumber'],  # e.g., 112.02.002-1
            'Parent': parent_id,  # Parent is Level 4
            'Name': row['UnitName'],  # Name of the unit
            'Level': 5,
            'Size': row['Members']  # Total members as size
        })

    # Step 8: Convert tree data to DataFrame
    tree_df = pd.DataFrame(tree_data)

    # Step 9: Create the tree diagram with sizes
    fig = px.treemap(
        tree_df,
        path=['Parent', 'ID'],  # Defines the hierarchy
        values='Size',  # Node size based on Members
        hover_name='Name',  # Hover shows the unit name
        title=f"Hierarchy Tree Diagram with Sizes for {selected_year}",
    )
    return fig
