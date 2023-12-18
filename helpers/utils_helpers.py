import pandas as pd
import json
import numpy as np
import requests
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from urllib.parse import quote


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

def fetch_pageview_count(language, articles, granularity = "monthly", start = "20180101", end = "20230101"):
    api_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}"

    params = {
        "project": f"{language}.wikipedia",   # Language-specific Wikipedia project
        "access": "all-access",
        "agent": "user",
        "granularity": granularity,
        "start": start,
        "end": end
    }

    headers = {
        "User-Agent": "WikiWackyNews"
    }

    pageviews_data = {}

    for article in articles:
        params["article"] = article

        # Make the API request
        response = requests.get(api_url.format(**params), headers=headers)
        
        # Access the data and save it as a dataframe
        if response.status_code == 200:
            data = response.json()
            item_list = data.get("items", [])
            
            if item_list:
                df = pd.DataFrame(item_list).copy()
                df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y%m%d%H')
                pageviews_data[article] = df
            else:
                print(f"No data available for {article}")
        else:
            print(f"Error fetching data for {article}. Status Code: {response.status_code}")

    return pageviews_data

# def scrape_wikipedia_page(article_title, language="en"):
#     # Replace spaces with underscores for Wikipedia URL format
#     article_title_url = article_title.replace(' ', '_')

#     # Wikipedia base URL
#     base_url = f'https://{language}.wikipedia.org/wiki/'

#     # Full URL to scrape
#     full_url = base_url + article_title_url

#     # Send a GET request to the Wikipedia page
#     response = requests.get(full_url)

#     # Check if the page was retrieved successfully
#     if response.status_code == 200:
#         # Parse the content of the request with BeautifulSoup
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # DataFrame to store the headings, subheadings, sub-subheadings, and links
#         headings_df = pd.DataFrame(columns=['Sub-subheading', 'Subheading', 'Main Heading', 'Links'])

#         # Initialize current headings
#         current_main_heading = None
#         current_sub_heading = None
#         current_sub_subheading = None
#         index = 0

#         # Iterate through all heading tags
#         for tag in soup.find_all(['h2', 'h3', 'h4', 'p', 'a']):
#             # # Remove the '[edit]' part from the text
#             # text = tag.get_text().replace('[edit]', '').strip()
#             # Remove the '[edit]' part from the text
#             text = tag.get_text().split('[')[0].strip()

#             # Determine tag type and process accordingly
#             if tag.name == 'h2':
#                 current_main_heading = text
#             elif tag.name == 'h3':
#                 current_sub_heading = text
#                 # Reset sub-subheading when a new subheading is found
#                 current_sub_subheading = None
#                 # Add the subheading to the dataframe
#                 headings_df.loc[index] = [text, current_sub_heading, current_main_heading, []]
#                 index += 1
#                 # headings_df = headings_df.append({
#             elif tag.name == 'h4':
#                 current_sub_subheading = text
#                 # Add the sub-subheading to the dataframe
#                 headings_df.loc[index] = [text, current_sub_heading, current_main_heading, []]
#                 index += 1
#             elif tag.name == 'a' and 'href' in tag.attrs:
#                 # Check if the link is a valid article link
#                 link = tag['href']
#                 if link.startswith('/wiki/') and ':' not in link:
#                     # Add the link to the appropriate heading in the dataframe
#                     if current_sub_subheading:
#                         headings_df.loc[headings_df['Sub-subheading'] == current_sub_subheading, 'Links'].apply(lambda x: x.append(link))
#                     elif current_sub_heading:
#                         headings_df.loc[headings_df['Subheading'] == current_sub_heading, 'Links'].apply(lambda x: x.append(link))
#         return headings_df
#     else:
#         # Return an empty DataFrame if the page could not be retrieved
#         return pd.DataFrame()
