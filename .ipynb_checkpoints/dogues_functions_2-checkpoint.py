import re
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import json
from pylab import *
import pandas as pd

def clean_article_name(article):
    # Remove the year from the article name using regular expressions
    return re.sub(r'\([^)]*\)', '', article).strip()

def plot_category_trends(df, use_log_scale=True):
    """
    Plots the trends of each category in the DataFrame over time.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing the data.
    - use_log_scale (bool): Flag indicating whether to use a logarithmic scale for the y-axis. Default is True.

    Returns:
    - None: Displays the plot.
    """

    # Transpose the DataFrame for easier plotting
    df_transposed = df.iloc[:, :-2].transpose()

    # Plot each category with or without a logarithmic scale
    plt.figure(figsize=(10, 6))  # Adjust the figure size as needed

    for category in df_transposed.columns:
        if use_log_scale:
            plt.semilogy(df_transposed.index, df_transposed[category], label=category)
        else:
            plt.plot(df_transposed.index, df_transposed[category], label=category)

    # Add labels and title
    plt.xlabel('Date')
    plt.ylabel('Logarithmic Value' if use_log_scale else 'Value')
    plt.title('Category Trends Over Time' + (' (Logarithmic Scale)' if use_log_scale else ''))

    # Add a legend
    plt.legend()

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Show the plot
    plt.tight_layout()
    
    # Update ylabel to indicate logarithmic scale
    if use_log_scale:
        plt.yscale('log')
        plt.ylabel('Logarithmic Value')

    plt.show()

def fetch_pageview_count(language, articles):
    api_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}"

    params = {
        "project": f"{language}.wikipedia",   # Language-specific Wikipedia project
        "access": "all-access",
        "agent": "user",
        "granularity": "daily",
        "start": "20190101",
        "end": "20230531"
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


def normal_data(list_data):
    max_val = max(list_data)
    norm   = array(list_data)/max_val
    return norm

# Cleaning the clusters to only obtain words searcheable in wikipedia API
def extract_clean_text(links):
    cleaned_links = []
    for link in links:
        if '/wiki/' in link:
            extracted_text = link.split('/wiki/')[1].split('#')[0].replace('_', ' ')
            cleaned_links.append(extracted_text)
    return cleaned_links


def fetch_and_combine_pageview_data(language, input_df):
    """
    Fetches pageview count data for each article in the input DataFrame and combines the data into a new DataFrame.

    Parameters:
    - language (str): Language code for the Wikipedia page.
    - input_df (pd.DataFrame): Input DataFrame containing articles.

    Returns:
    - pd.DataFrame: Combined DataFrame with pageview count data.
    """

    # Create an empty DataFrame to store the combined data
    combined_df = pd.DataFrame()

    # Iterate through the list of articles
    for i in range(len(input_df['Linked_Article'])):
        try:
            # Fetch pageview count data for the current article
            articles_list = [input_df['Linked_Article'].iloc[i]]
            result = fetch_pageview_count(language, articles_list)  # Assuming fetch_pageview_count is a defined function

            # Extract relevant data and append it to the combined DataFrame
            if input_df['Linked_Article'].iloc[i] in result:
                current_df = result[input_df['Linked_Article'].iloc[i]].drop(['project', 'granularity', 'access', 'agent'], axis=1)
                current_df['article'] = input_df['Linked_Article'].iloc[i]
                combined_df = pd.concat([combined_df, current_df], ignore_index=True)

        except Exception as e:
            print(f"Error fetching data for {input_df['Linked_Article'].iloc[i]}: {e}")

    return combined_df


def scrape_wikipedia_sub_subheadings_with_links(article_title):
    # Replace spaces with underscores for Wikipedia URL format
    article_title_url = article_title.replace(' ', '_')

    # Wikipedia base URL
    base_url = 'https://en.wikipedia.org/wiki/'

    # Full URL to scrape
    full_url = base_url + article_title_url

    # Send a GET request to the Wikipedia page
    response = requests.get(full_url)

    # Check if the page was retrieved successfully
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # DataFrame to store the headings, subheadings, sub-subheadings, and links
        headings_df = pd.DataFrame(columns=['Sub-subheading', 'Subheading', 'Main Heading', 'Linked_Article', 'Linked_Article_Link'])

        # Initialize current headings
        current_main_heading = None
        current_sub_heading = None
        current_sub_subheading = None

        # Iterate through all heading tags
        for tag in soup.find_all(['h2', 'h3', 'h4', 'p', 'a']):
            # Remove the '[edit]' part from the text
            text = tag.get_text().replace('[edit]', '').strip()
            # Determine tag type and process accordingly
            if tag.name == 'h2':
                current_main_heading = text
                current_sub_heading = None
                current_sub_subheading = None
            elif tag.name == 'h3':
                current_sub_heading = text
                current_sub_subheading = None
            elif tag.name == 'h4':
                current_sub_subheading = text
            elif tag.name == 'a' and 'href' in tag.attrs:
                # Check if the link is a valid article link
                link = tag['href']
                if link.startswith('/wiki/') and ':' not in link:
                    # Add the link to the dataframe along with the current headings
                    new_row = {
                        'Sub-subheading': current_sub_subheading,
                        'Subheading': current_sub_heading,
                        'Main Heading': current_main_heading,
                        'Linked_Article': link[len('/wiki/'):],
                        'Linked_Article_Link': base_url + link[len('/wiki/'):]
                    }
                    headings_df = pd.concat([headings_df, pd.DataFrame([new_row])], ignore_index=True)

        return headings_df
    else:
        # Return an empty DataFrame if the page could not be retrieved
        return pd.DataFrame()
    
def fetch_pageview_count_dates(language, articles, start_date = "20220101", end_date ="20230101", granularity = "daily"):
    api_url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/{project}/{access}/{agent}/{article}/{granularity}/{start}/{end}"

    params = {
        "project": f"{language}.wikipedia",   # Language-specific Wikipedia project
        "access": "all-access",
        "agent": "user",
        "granularity": granularity,
        "start": start_date,
        "end": end_date
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
                
def fetch_viewcount_df(df, language = "en"):
  # Example usage:
  language = "en"

  # Create an empty DataFrame to store the combined data
  combined_df = pd.DataFrame()

  # Iterate through the list of articles
  for i in range(len(df['Linked_Article'])):
      try:
          # Fetch pageview count data for the current article
          articles_list = [df['Linked_Article'].iloc[i]]
          result = fetch_pageview_count_dates(language, articles_list, start_date = "20200113", end_date = "20200420")

          # Extract relevant data and append it to the combined DataFrame
          if df['Linked_Article'].iloc[i] in result:
              current_df = result[df['Linked_Article'].iloc[i]].drop(['project', 'granularity', 'access', 'agent'], axis=1)
              current_df['article'] = df['Linked_Article'].iloc[i]
              combined_df = pd.concat([combined_df, current_df], ignore_index=True)

      except Exception as e:
          print(f"Error fetching data for {df['Linked_Article'].iloc[i]}: {e}")

  return combined_df



