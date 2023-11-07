import pandas as pd

def import_json_to_df(file_path, sub_sample=False):
    """
    Imports a JSON file into a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the JSON file.
    - sub_sample (bool): If True, imports only the first fifty lines of the JSON file.

    Returns:
    - DataFrame: A pandas DataFrame containing the imported data.
    """
    # Load the entire JSON file
    df = pd.read_json(file_path, lines=True)
    
    # If sub_sample is True, return only the first fifty rows
    if sub_sample:
        return df.head(50)
    
    return df

def import_csv_to_df(file_path, sub_sample=False):
    """
    Imports a CSV file into a pandas DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.
    - sub_sample (bool): If True, imports only the first fifty lines of the CSV file.

    Returns:
    - DataFrame: A pandas DataFrame containing the imported data.
    """
    # Read the CSV file. If sub_sample is True, read only the first 50 rows
    df = pd.read_csv(file_path, nrows=50 if sub_sample else None)
    
    return df