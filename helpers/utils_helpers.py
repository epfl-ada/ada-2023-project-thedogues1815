import pandas as pd
import json
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import quote
from ast import literal_eval



def spaces_to_underscore(df, column):
    df[column] = df[column].str.replace(" ", "_")
    return df

def import_json_to_df(json_file_path, exclude_fields = None, sub_sample=None):
    data = []  # List to store the processed records
    counter = 0  # Counter to keep track of the number of processed items

    # Open the file and process line by line
    with open(json_file_path, 'r') as file:
        for line in file:
            # Load the line as a JSON object
            json_object = json.loads(line.strip())
            
            # Exclude specified fields
            if exclude_fields != None:
              for field in exclude_fields:
                  json_object.pop(field, None)
            
            # Append the modified object to our data list
            data.append(json_object)
            counter += 1
            
            # Break if the sub_sample size is reached
            if sub_sample is not None and counter >= sub_sample:
                break
            
    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)
    
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

def info(df, info = False):
    for key in df.keys():
      perc_nan = np.sum(df[key].isna()) / len(df[key])
      print("% of NaN values of ", key, " is ", perc_nan)
    if info:
      df.info()
    return

def normal_data(list_data):
    max_val = max(list_data)
    norm   = np.array(list_data)/max_val
    return norm

def read_csv_convert_list(csv_file, list_columns):
    """
    Read a CSV file and convert specified columns from string representations of lists to actual lists.

    :param csv_file: Path to the CSV file.
    :param list_columns: List of column names that need to be converted from strings to lists.
    :return: Pandas DataFrame with converted columns.
    """
    df = pd.read_csv(csv_file)

    for column in list_columns:
        if column in df.columns:
            df[column] = df[column].apply(literal_eval)
        else:
            print(f"Column {column} not found in the DataFrame.")

    return df