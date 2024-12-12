import pandas as pd
import plotly.express as px

def add_hierarchy_levels(df):
    """
    Add hierarchy level columns to the DataFrame based on the RegistrationNumber column.
    """
    # Split on '.' and handle the main levels
    df['Level0'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[0] if len(x) > 0 else None)
    df['Level1'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[0] if len(x) > 0 else None)
    df['Level2'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[1] if len(x) > 1 else None)
    df['Level3'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[2].split('-')[0] if len(x) > 2 else None)
    df['Level4'] = df['RegistrationNumber'].str.extract(r'-(\\d+)$', expand=False)

    # Only fill NaN and convert to string for hierarchy levels
    hierarchy_columns = ['Level0', 'Level1', 'Level2', 'Level3', 'Level4']
    df[hierarchy_columns] = df[hierarchy_columns].fillna('').astype(str)

    return df
