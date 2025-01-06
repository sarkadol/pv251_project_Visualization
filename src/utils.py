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

def add_hierarchy_levels_whole(df):
    """
    Add hierarchy level columns to the DataFrame based on the RegistrationNumber column.
    """
    # Ensure RegistrationNumber is a string
    df['RegistrationNumber'] = df['RegistrationNumber'].fillna('').astype(str)

    # Extract hierarchy levels
    df['LevelKrajWhole'] = df['RegistrationNumber'].apply(lambda x: x[:2] if len(x) > 0 else 'Unknown')
    df['LevelOkresWhole'] = df['RegistrationNumber'].apply(lambda x: x[:3] if len(x) > 0 else 'Unknown')
    df['LevelStrediskoWhole'] = df['RegistrationNumber'].apply(lambda x: x[:6] if len(x) > 0 else 'Unknown')
    df['LevelOddilWhole'] = df['RegistrationNumber'].apply(lambda x: x[:10] if len(x) > 0 else 'Unknown')
    df['LevelDruzinaWhole'] = df['RegistrationNumber'].fillna('Unknown')


    return df

def add_hierarchy_levels_text(df):
    """
    Add hierarchy level columns to the DataFrame based on the RegistrationNumber column.
    """
    df =df.copy()
    # Ensure RegistrationNumber is a string
    df['RegistrationNumber'] = df['RegistrationNumber'].fillna('').astype(str)

    registration_dict = df.set_index('RegistrationNumber')['UnitName'].to_dict()

    # Extract hierarchy levels
    def add_hierarchy_levels_text(df):
        """
        Add hierarchy level columns to the DataFrame based on the RegistrationNumber column using a dictionary.
        """
    # Make a copy to avoid modifying the original DataFrame
    df = df.copy()

    # Ensure RegistrationNumber is a string
    df['RegistrationNumber'] = df['RegistrationNumber'].fillna('').astype(str)

    # Create the dictionary for fast lookups
    registration_dict = df.set_index('RegistrationNumber')['UnitName'].to_dict()

    # Use the dictionary for hierarchy levels
    df['LevelKrajWhole'] = df['RegistrationNumber'].apply(lambda x: registration_dict.get(x[:2]+"0", ' ') if len(x) > 1 else ' ')
    df['LevelOkresWhole'] = df['RegistrationNumber'].apply(lambda x: registration_dict.get(x[:3], ' ') if len(x) > 2 else ' ')
    df['LevelStrediskoWhole'] = df['RegistrationNumber'].apply(lambda x: registration_dict.get(x[:6], ' ') if len(x) > 5 else ' ')
    df['LevelOddilWhole'] = df['RegistrationNumber'].apply(lambda x: registration_dict.get(x[:10], ' ') if len(x) > 9 else ' ')
    df['LevelDruzinaWhole'] = df['RegistrationNumber'].fillna(' ')  # Assuming DruzinaWhole is the full RegistrationNumber
    df.to_csv('new_dataframe.csv', index=False)

    return df

def get_kraj_name(kraj_value, merged_dataframe):
    print("kraj_value",kraj_value)
    unit_row = merged_dataframe[merged_dataframe['RegistrationNumber'] == kraj_value]
    if not unit_row.empty:
        return unit_row.sort_values(by='Year', ascending=False)['UnitName'].iloc[0]
    return 'Unknown'

def get_okres_name(okres_value, merged_dataframe):
    unit_row = merged_dataframe[merged_dataframe['RegistrationNumber'] == okres_value]
    if not unit_row.empty:
        return unit_row.sort_values(by='Year', ascending=False)['UnitName'].iloc[0]
    return 'Unknown'

def get_stredisko_name(stredisko_value, merged_dataframe):
    unit_row = merged_dataframe[merged_dataframe['RegistrationNumber'] == stredisko_value]
    if not unit_row.empty:
        return unit_row.sort_values(by='Year', ascending=False)['UnitName'].iloc[0]
    return 'Unknown'

def get_oddil_name(oddil_value, merged_dataframe):
    unit_row = merged_dataframe[merged_dataframe['RegistrationNumber'] == oddil_value]
    if not unit_row.empty:
        return unit_row.sort_values(by='Year', ascending=False)['UnitName'].iloc[0]
    return 'Unknown'

