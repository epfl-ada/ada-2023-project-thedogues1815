import requests
import pandas as pd 
from bs4 import BeautifulSoup
from urllib.parse import unquote  # Import the unquote function
from googletrans import Translator
from urllib.parse import quote  # Import quote for URL encoding
import ast
from ast import literal_eval
from pylab import  * 


def fetch_pageview_count_Antonio(language, articles):
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


def wiki_extract_time_increase(wiki_pages_links, word_cluster_1, language, year_control ):
    wiki_cluster_links_1 = wiki_pages_links[(wiki_pages_links["Main Heading"].str.contains(word_cluster_1))].copy()
    
    # Cleaning the clusters to only obtain words searcheable in wikipedia API
    def extract_clean_text(links):
        cleaned_links = []
        for link in links:
            if '/wiki/' in link:
                extracted_text = link.split('/wiki/')[1].split('#')[0].replace('_', ' ')
                cleaned_links.append(extracted_text)
        return cleaned_links
    
    # Convert string representation of list to actual list using ast.literal_eval and apply the function
    wiki_cluster_links_1["Cleaned_Text"] = wiki_cluster_links_1["Links"].apply(lambda x: extract_clean_text(ast.literal_eval(x)))
    
    # Looking for all the articles in the cluster 1 which correspond to Virus Origin 
    
    list_cluster_1 = list(wiki_cluster_links_1["Cleaned_Text"])
    
    final_count_1 =[]
    for i in list_cluster_1:
        results   = fetch_pageview_count_Antonio(language, i )
        merged_df = pd.concat(results, ignore_index=True)
        #Grouping the dataframe to sum up the views
        merged_df = merged_df.groupby(['timestamp'])["views"].sum()
        final_count_1.append(pd.DataFrame(merged_df))
        
    final_views_1= pd.concat(final_count_1, ignore_index=False) 
    data_1 = final_views_1.groupby(['timestamp']).sum()
    data_1['time_1'] = pd.to_datetime(data_1.index, format='%d/%m/%Y')
    if year_control==2019:
        start_date_i = 0   #2019
        final_date_i = 365  #2019
        start_date_f = 365  #2020
        final_date_f = 365*2#2020
    elif year_control==2022:
        start_date_i = 365*3  #2022
        final_date_i = 365*4  #2022
        start_date_f = 365    #2020
        final_date_f = 365*2  #2020
    
    time_1         = data_1["time_1"][start_date_i:final_date_i]
    time_2         = data_1["time_1"][start_date_f:final_date_f]
    base_line      = array(data_1["views"][start_date_i:final_date_i])
    increase       = array(data_1["views"][start_date_f:final_date_f])
    
    return time_1 , time_2, base_line, increase
    
def intervention_date(intervention_data, intervention_event):
    year  = int(intervention_data[intervention_event][0:4])
    month = int(intervention_data[intervention_event][5:7])
    day   = int(intervention_data[intervention_event][8:10])
    date  = datetime.datetime(year, month, day)
    return date

def get_pageview_period(time,page_view, days, date,status):
    # Replace this with your actual lists of dates and visits
    dates_list  = list(time)
    visits_list = list(log(array(page_view)))
    
    # Specific date to split the data
    specific_date = date
    
    # Create a DataFrame from the lists
    df = pd.DataFrame({'Date': dates_list, 'Visits': visits_list})
    
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Find the index of the specific date
    specific_date_index = df[df['Date'] == specific_date].index[0]
    
    # Select 50 days before and after the specific date
    date_range = pd.date_range(start=specific_date - pd.Timedelta(days=days), end=specific_date + pd.Timedelta(days=days))
    
    # Create a new column 'Period' to label pre/post specific date
    df['Period'] = 'Pre'  # Initialize as 'Pre'
    df['Treated'] = status
    df.loc[df['Date']>specific_date, 'Period'] = 'Post'  # Set 'Post' for dates within the range
    
    # Filter the DataFrame to include only the 50 days before and after the specific date
    filtered_df = df[df['Date'].isin(date_range)]
    
    return filtered_df

def get_standard_error_sum(results, covariates):
    '''
    #95CI is approximated with +- 2 sum_variance_standard_error
    '''
    # get the variance covariance matrix
    # print(covariates)
    vcov = results.cov_params() \
        .loc[covariates, covariates].values

    # calculate the sum of all pair wise covariances by summing up off-diagonal entries
    off_dia_sum = np.sum(vcov)
    # variance of a sum of variables is the square root
    return np.sqrt(off_dia_sum)


def clean_df_wikilinks(wiki_pages_links):
    empty_rows = []
    for i in  range(0,len(wiki_pages_links["Links"])):
        if wiki_pages_links["Links"].iloc[i]=="[]":
            empty_rows.append(i)
    wiki_pages_links.drop(empty_rows, axis=0, inplace=True)
    return wiki_pages_links


def fetch_pageview_count(language, articles, start_date = "20180101", end_date ="20200630", granularity = "daily"):
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


def fetch_viewcount_df(df, column = 'Page', language = "en", start_date = "20200113", end_date = "20200420", granularity = "monthly", wiki = False):
  # Create an empty DataFrame to store the combined data
  combined_df = pd.DataFrame()

  # Iterate through the list of articles
  for i in range(len(df[column])):
    try:
          # Fetch pageview count data for the current article
        articles_list = [df[column].iloc[i]]
        result = fetch_pageview_count(language, articles_list, start_date, end_date, granularity)

          # Extract relevant data and append it to the combined DataFrame
        if df[column].iloc[i] in result:
            current_df = result[df[column].iloc[i]].drop(['project', 'granularity', 'access', 'agent'], axis=1)
            current_df['article'] = df[column].iloc[i]
            combined_df = pd.concat([combined_df, current_df], ignore_index=True)

    except Exception as e:
          print(f"Error fetching data for {df[column].iloc[i]}: {e}")

    return combined_df

def scrape_wikipedia_page(article_title, language="en"):
    # Replace spaces with underscores and decode for Wikipedia URL format
    article_title_url = unquote(article_title.replace(' ', '_'))

    # Wikipedia base URL
    base_url = f'https://{language}.wikipedia.org'

    # Full URL to scrape
    full_url = base_url + '/wiki/' + article_title_url

    # Send a GET request to the Wikipedia page
    response = requests.get(full_url)

    # Check if the page was retrieved successfully
    if response.status_code == 200:
        # Parse the content of the request with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # DataFrame to store the headings, subheadings, sub-subheadings, original links and full links
        headings_df = pd.DataFrame(columns=['Sub-subheading', 'Subheading', 'Main Heading', 'Links', 'Full Links'])

        # Initialize current headings
        current_main_heading = None
        current_sub_heading = None
        current_sub_subheading = None
        index = 0

        # Iterate through all heading tags
        for tag in soup.find_all(['h2', 'h3', 'h4', 'p', 'a']):
            # Remove the '[edit]' part from the text
            text = tag.get_text().split('[')[0].strip()

            # Determine tag type and process accordingly
            if tag.name == 'h2':
                current_main_heading = text
            elif tag.name == 'h3':
                current_sub_heading = text
                current_sub_subheading = None
                headings_df.loc[index] = [text, current_sub_heading, current_main_heading, [], []]
                index += 1
            elif tag.name == 'h4':
                current_sub_subheading = text
                headings_df.loc[index] = [text, current_sub_heading, current_main_heading, [], []]
                index += 1
            elif tag.name == 'a' and 'href' in tag.attrs:
                # Decode the link and check if it is a valid article link
                link = unquote(tag['href'])
                if link.startswith('/wiki/') and ':' not in link:
                    full_link = base_url + link  # Prepend the base URL to the link
                    # Add the link and full link to the appropriate heading in the dataframe
                    if current_sub_subheading:
                        headings_df.loc[headings_df['Sub-subheading'] == current_sub_subheading, 'Links'].apply(lambda x: x.append(link))
                        headings_df.loc[headings_df['Sub-subheading'] == current_sub_subheading, 'Full Links'].apply(lambda x: x.append(full_link))
                    elif current_sub_heading:
                        headings_df.loc[headings_df['Subheading'] == current_sub_heading, 'Links'].apply(lambda x: x.append(link))
                        headings_df.loc[headings_df['Subheading'] == current_sub_heading, 'Full Links'].apply(lambda x: x.append(full_link))
        return headings_df
    else:
        # Return an empty DataFrame if the page could not be retrieved
        return pd.DataFrame()

def get_wiki_titles(url, target_language='en'):
    # Extract the language and URL-decoded title from the URL
    split_url = url.split('/')
    language_code = split_url[2].split('.')[0]  # Extract language code from the domain
    title = unquote(split_url[-1])  # URL-decode the title

    # Define the Wikipedia API endpoint for the language of the original article
    api_endpoint = f"https://{language_code}.wikipedia.org/w/api.php"

    # Set up the parameters for the query
    params = {
        'action': 'query',
        'format': 'json',
        'titles': title,
        'prop': 'langlinks',
        'lllimit': 'max'
    }

    # Make the request
    response = requests.get(api_endpoint, params=params)

    # Check if the response is successful
    if response.status_code == 200:
        try:
            data = response.json()
            pages = data['query']['pages']
            page_id = next(iter(pages))  # Get the first page id
            langlinks = pages[page_id].get('langlinks', [])

            # Find the title in the target language in the langlinks
            for link in langlinks:
                if link['lang'] == target_language:
                    return link['*']

            print(f"No article found in {target_language}")
            return None
        except KeyError:
            print("Unexpected API response format")
            return None
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        return None


def translate_dataframe_columns(df, columns, dest_lang='en'):
    translator = Translator()
    
    for column in columns:
        translated_texts = []
        for text in df[column]:
            try:
                translated = translator.translate(text, dest=dest_lang)
                translated_texts.append(translated.text)
            except Exception as e:
                print(f"Error translating text in column '{column}': {e}")
                translated_texts.append(text)  # Keep the original text in case of error

        df[column + '_translated'] = translated_texts

    return df

def get_english_wiki_titles(df, link_column='Full Links', new_full_link_column='English Full Links', new_relative_link_column='English Relative Links'):
    # Create new columns in the DataFrame
    english_titles_df = df.copy()
    english_titles_df[new_full_link_column] = None
    english_titles_df[new_relative_link_column] = None

    for index, row in english_titles_df.iterrows():
        english_full_links = []
        english_relative_links = []

        for article_url in row[link_column]:
            # Assuming the URLs in 'Full_Links' are complete URLs to Wikipedia articles
            titles = get_wiki_titles(article_url, 'en')
            english_title = titles if titles else None  # Get English title if available

            if english_title:
                # Replace spaces with underscores and encode the title for URL
                encoded_english_title = quote(english_title.replace(' ', '_'))

                # Construct a full URL and a relative URL with the English title
                english_full_url = f'https://en.wikipedia.org/wiki/{encoded_english_title}'
                english_relative_url = f'/wiki/{encoded_english_title}'

                english_full_links.append(english_full_url)
                english_relative_links.append(english_relative_url)
            else:
                # If no English version is found, keep the original URL in both columns
                english_full_links.append(article_url)
                english_relative_links.append(article_url)  # or leave it empty if preferred

        english_titles_df.at[index, new_full_link_column] = english_full_links
        english_titles_df.at[index, new_relative_link_column] = english_relative_links

    return english_titles_df

def multi_lang_df(url = "https://en.wikipedia.org/wiki/COVID-19_misinformation", languages = ['fr', 'es', 'it']):
    titles = {'en': "COVID-19_misinformation"}
    for language in languages:
        titles[language] = get_wiki_titles(url, language)

    headings_dict = {"en": pd.DataFrame(), "fr": pd.DataFrame(), "es": pd.DataFrame(), "it": pd.DataFrame()}

    for i in range(len(titles)-1):
        language = str(languages[i])
        article_title = titles[language]

        if language == "en":
            # Extract the wiki page, we use English as the reference language
            final_page = scrape_wikipedia_page(article_title, language=language)
        else:
            # Extract the wiki page
            raw_page = scrape_wikipedia_page(article_title, language=language)

            # Remove uninteresting parts
            if language == "it":
                raw_page = raw_page[raw_page['Main Heading'] != 'Menu di navigazione']
            if language == "fr":
                raw_page = raw_page[raw_page['Main Heading'] != 'Voir aussi']

            # Translate the original page to English
            translated_page = translate_dataframe_columns(df=raw_page, columns=["Main Heading", "Subheading", "Sub-subheading"])
            # Get the equivalent English articles for comparison
            final_page = get_english_wiki_titles(translated_page)

        headings_dict[language] = final_page

    return headings_dict


