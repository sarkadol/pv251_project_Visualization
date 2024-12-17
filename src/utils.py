import pandas as pd
import plotly.express as px

def add_hierarchy_levels(df):
    """
    Add hierarchy level columns to the DataFrame based on the RegistrationNumber column.
    """
    # Ensure RegistrationNumber is a string
    df['RegistrationNumber'] = df['RegistrationNumber'].fillna('').astype(str)

    # Extract hierarchy levels
    df['LevelKraj'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[0][:2] if len(x) > 0 else 'Unknown')
    df['LevelOkres'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[0] if len(x) > 0 else 'Unknown')
    df['LevelStredisko'] = df['RegistrationNumber'].str.split('.').apply(lambda x: x[1] if len(x) > 1 else 'Unknown')
    df['LevelOddil'] = df['RegistrationNumber'].str.split('.').apply(
        lambda x: x[2].split('-')[0] if len(x) > 2 and '-' in x[2] else 'Unknown'
    )
    df['LevelDruzina'] = df['RegistrationNumber'].str.extract(r'-(\d+)$', expand=False).fillna('Unknown')


    return df
