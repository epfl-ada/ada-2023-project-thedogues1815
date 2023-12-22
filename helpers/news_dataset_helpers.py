
import pandas as pd
import json
import numpy as np
import requests
import matplotlib.pyplot as plt
import sys
import re
from bs4 import BeautifulSoup
from ast import literal_eval


# Antonio imports
from datetime import datetime, timedelta
from matplotlib.dates import AutoDateLocator, DateFormatter
import plotly.express as px
from pylab import  * 
import ast
from datetime import datetime, timedelta
# from dateutil.relativedelta import relativedelta
import statsmodels.formula.api as smf
import pandas as pd
import statsmodels

#Tecla imports
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer
from supersmoother import SuperSmoother
from sklearn.metrics import jaccard_score
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib_venn import venn2
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler
from wordcloud import WordCloud
from matplotlib.patches import Rectangle


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


# Function for text preprocessing (remove non-alphabetic characters, remove stopwords, lowercase, and stemming)

def preprocess_text(text):
    ps = PorterStemmer()
    stop_words = ENGLISH_STOP_WORDS
    words = re.findall(r'\b\w+\b', text.lower())
    filtered_words = [ps.stem(word) for word in words if word not in stop_words]
    return filtered_words

# Function to generate BoW 

def generate_bow_for_heading(df, heading):
    
    # Filter misinformation DataFrame for the specific heading
    misinformation_subset = df[df['Main Heading'] == heading]
    misinformation_subset = misinformation_subset.dropna()
    
    misinformation_text = misinformation_subset[['Sub-subheading', 'Subheading', 'Main Heading']].apply(
    lambda x: ' '.join(x.dropna().astype(str)), axis=1
)
    misinformation_text = misinformation_text.dropna()
    misinformation_words_preprocessed = misinformation_text.apply(preprocess_text)
    
  
    
    # Manually remove specific words from the list
    words_to_remove = ['19', 'covid', 'cov', '2020', '2019', 'urin', 'gain','use']
   #                'count', 'urin', 'oil', 'govern','nation', 'state', 'spread', 'heal', 
   #                    'gain', 'world', 'report', 'medic', 'countri', 'death', 'news', 
   #                    'diseas','safe','immun','transmiss','larg', 'base', 'prevent', 'treatment', 'flu', 
   #                   'bodi', 'remain','predict', 'chloroquin','popul', 'claim',, 'caus','social','relat']
    misinformation_flat_words = [
    word for words_list in misinformation_words_preprocessed for word in words_list if word not in words_to_remove
    ]
    # Create a CountVectorizer instance
    vectorizer = CountVectorizer()

    # Fit and transform the preprocessed words to obtain the BoW matrix
    X_bow_misinformation = vectorizer.fit_transform([' '.join(misinformation_flat_words)])

    # Access the feature names (words)
    feature_names = vectorizer.get_feature_names()
    #print(feature_names)

    # Convert the BoW matrix to a DataFrame for easier exploration
    bow_misinformation_df = pd.DataFrame(X_bow_misinformation.toarray(), columns=feature_names)


    return bow_misinformation_df, feature_names


# Function to generate BoW 

def generate_bow_for_heading_noneng(df, heading):
    
    # Filter misinformation DataFrame for the specific heading
    misinformation_subset = df[df['Main Heading_translated'] == heading]
    misinformation_subset = misinformation_subset.dropna()
    
    misinformation_text = misinformation_subset[['Sub-subheading_translated', 'Subheading_translated', 'Main Heading_translated']].apply(
    lambda x: ' '.join(x.dropna().astype(str)), axis=1
)
    misinformation_text = misinformation_text.dropna()
    misinformation_words_preprocessed = misinformation_text.apply(preprocess_text)
    
  
    
    # Manually remove specific words from the list
    words_to_remove = ['19', 'covid', 'cov', '2020', '2019', 'corona','coronaviru', 'spi', 'use', 'hot','face', 'urin'
                     'oil', 'govern','nation', 'state', 'heal', 
                       'gain', 'world', 'report', 'medic', 'countri', 
                       'diseas','safe','immun','larg', 'base', 'treatment', 'flu', 
                      'bodi', 'remain','predict', 'chloroquin','popul', 'pandem','epidem', 'new', 'aid', 'basi']
    misinformation_flat_words = [
    word for words_list in misinformation_words_preprocessed for word in words_list if word not in words_to_remove
    ]
    # Create a CountVectorizer instance
    vectorizer = CountVectorizer()

    # Fit and transform the preprocessed words to obtain the BoW matrix
    X_bow_misinformation = vectorizer.fit_transform([' '.join(misinformation_flat_words)])

    # Access the feature names (words)
    feature_names = vectorizer.get_feature_names()
    #print(feature_names)

    # Convert the BoW matrix to a DataFrame for easier exploration
    bow_misinformation_df = pd.DataFrame(X_bow_misinformation.toarray(), columns=feature_names)


    return bow_misinformation_df, feature_names



'''
#Function to plot the subcatogory pies
def plot_subcategory_pie(subcategory_counts_by_heading, tot_news):
    num_headings = len(subcategory_counts_by_heading)

    # Determine the number of rows and columns for the grid
    if num_headings == 3:
        nrows, ncols = 1, 3
    elif num_headings == 4:
        nrows, ncols = 2, 2
    elif num_headings == 5:
        nrows, ncols = 2, 3
    elif num_headings == 6:
        nrows, ncols = 2, 3
    elif num_headings == 7:
        nrows, ncols = 3, 3
    else:
        raise ValueError("Unsupported number of headings")

    # Plot the charts in a grid
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10))

    # Iterate over the headings
    for i, (heading, subcategory_counts) in enumerate(subcategory_counts_by_heading.items()):
        if i >= num_headings:
            break  
        
        
        if nrows == 1:
            col = i
            
            axes[col].pie(subcategory_counts, labels=subcategory_counts.index, autopct='%1.1f%%', startangle=140)
            axes[col].set_title(f'{heading}\n{round(subcategory_counts.sum()/tot_news* 100)} % of news')


        else:
            row = i // ncols
            col = i % ncols

            axes[row, col].pie(subcategory_counts, labels=subcategory_counts.index, autopct='%1.1f%%', startangle=140)
            axes[row, col].set_title(f'{heading}\n{round(subcategory_counts.sum()/tot_news* 100)} % of news')

    # Plot the last chart in the center of the last row if there are 5 or 7 headings
    if num_headings == 5:
        last_heading, last_subcategory_counts = list(subcategory_counts_by_heading.items())[-1]
        axes[1, 1].pie(last_subcategory_counts, labels=last_subcategory_counts.index, autopct='%1.1f%%', startangle=140)
        axes[1, 1].set_title(f'{last_heading}\n{round(last_subcategory_counts.sum()/tot_news* 100)} % of news')
        fig.delaxes(axes[1, 2])
        fig.delaxes(axes[1, 0])
        
    if num_headings == 7:
        last_heading, last_subcategory_counts = list(subcategory_counts_by_heading.items())[-1]
        axes[2, 1].pie(last_subcategory_counts, labels=last_subcategory_counts.index, autopct='%1.1f%%', startangle=140)
        axes[2, 1].set_title(f'{last_heading}\n{round(last_subcategory_counts.sum()/tot_news* 100)} % of news')
        fig.delaxes(axes[2, 2])
        fig.delaxes(axes[2, 0])
        
    plt.tight_layout()
    plt.show()
'''

def plot_subcategory_pie(subcategory_counts_by_heading, tot_news, top_n=10, exclude_categories={}):
    num_headings = len(subcategory_counts_by_heading)

    # Determine the number of rows and columns for the grid
    if num_headings == 3:
        nrows, ncols = 1, 3
    elif num_headings == 4:
        nrows, ncols = 2, 2
    elif num_headings == 5 or num_headings == 6:
        nrows, ncols = 2, 3
    elif num_headings == 7:
        nrows, ncols = 3, 3
    else:
        raise ValueError("Unsupported number of headings")

    # Plot the charts in a grid
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10))

    # Iterate over the headings
    for i, (heading, subcategory_counts) in enumerate(subcategory_counts_by_heading.items()):
        if i >= num_headings:
            break

        # Sort subcategories by count and select top N
        sorted_subcategories = sorted(subcategory_counts.items(), key=lambda x: x[1], reverse=True)

        # Exclude specified categories
        excluded_categories = exclude_categories.get(heading, [])
        filtered_subcategories = [(subcategory, count) for subcategory, count in sorted_subcategories if subcategory not in excluded_categories]
        top_subcategories = dict(filtered_subcategories[:top_n])

        if nrows == 1:
            col = i
            subcategory_names = list(top_subcategories.keys())
            subcategory_values = list(top_subcategories.values())

            axes[col].pie(subcategory_values, labels=subcategory_names, autopct='%1.1f%%', startangle=140)
            axes[col].set_title(f'{heading}\n{round(sum(subcategory_values)/tot_news* 100)} % of news')

        else:
            row = i // ncols
            col = i % ncols
            subcategory_names = list(top_subcategories.keys())
            subcategory_values = list(top_subcategories.values())

            axes[row, col].pie(subcategory_values, labels=subcategory_names, autopct='%1.1f%%', startangle=140)
            axes[row, col].set_title(f'{heading}\n{round(sum(subcategory_values)/tot_news* 100)} % of news')

    plt.tight_layout()
    plt.show()


def plot_subcategory_wordcloud(subcategory_counts_by_heading):
    num_headings = len(subcategory_counts_by_heading)

    # Determine the number of rows and columns for the grid
    if num_headings == 3:
        nrows, ncols = 1, 3
    elif num_headings == 4:
        nrows, ncols = 2, 2
    elif num_headings == 5:
        nrows, ncols = 2, 3
    elif num_headings == 6:
        nrows, ncols = 2, 3
    elif num_headings == 7:
        nrows, ncols = 3, 3
    else:
        raise ValueError("Unsupported number of headings")

    # Plot the word clouds in a grid
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 10))

    # Iterate over the headings
    for i, (heading, subcategory_counts) in enumerate(subcategory_counts_by_heading.items()):
        if i >= num_headings:
            break
        
        # Generate a dictionary where keys are subcategories and values are their counts
        subcategory_dict = subcategory_counts.to_dict()
        
        # Generate word cloud with word frequencies proportional to their counts
        wordcloud = WordCloud(width=400, height=400, background_color='white').generate_from_frequencies(subcategory_dict)
        
        if nrows == 1:
            col = i
            
            axes[col].imshow(wordcloud, interpolation='bilinear')
            axes[col].set_title(f'{heading}')
            rect = Rectangle((0, 0), 1, 1, transform=axes[col].transAxes, fill=False, edgecolor='black', linewidth=2)
            axes[col].add_patch(rect)
            axes[col].axis('off')

        else:
            row = i // ncols
            col = i % ncols
            
            axes[row, col].imshow(wordcloud, interpolation='bilinear')
            axes[row, col].set_title(f'{heading}')
            rect = Rectangle((0, 0), 1, 1, transform=axes[row, col].transAxes, fill=False, edgecolor='black', linewidth=2)
            axes[row, col].add_patch(rect)
            axes[row, col].axis('off')

    # Remove the unnecessary axes
    if num_headings == 5:
        fig.delaxes(axes[1, 2])
        fig.delaxes(axes[1, 0])
        
    if num_headings == 7:
        last_heading, last_subcategory_counts = list(subcategory_counts_by_heading.items())[-1]
        axes[2, 1].imshow(wordcloud, interpolation='bilinear')
        axes[2, 1].set_title(f'{last_heading}')
        rect = Rectangle((0, 0), 1, 1, transform=axes[2, 1].transAxes, fill=False, edgecolor='black', linewidth=2)
        axes[row, col].add_patch(rect)
        axes[2, 1].set_xticks([])
        axes[2, 1].set_yticks([])
        axes[2, 1].set_frame_on(True)
        fig.delaxes(axes[2, 2])
        fig.delaxes(axes[2, 0])
        

    plt.tight_layout()
    plt.show()

    
    
    
#Function to calculate jaccard similarity between 2 sets

def jaccard_similarity(set1, set2):
    intersection = set(set1).intersection(set2)
    union = set(set1).union(set2)
    return (len(intersection) / len(union))


# Function to calculate Cosine similarity
def cosine_similarity_score(set1, set2):
    # Convert sets to lists for sklearn's cosine_similarity
    list1, list2 = list(set1), list(set2)
    
    # Create binary vectors for each set based on presence/absence of elements
    vector1 = [1 if element in list1 else 0 for element in set1.union(set2)]
    vector2 = [1 if element in list2 else 0 for element in set1.union(set2)]
    
    # Reshape vectors to be 2D arrays for sklearn's cosine_similarity
    vector1, vector2 = [vector1], [vector2]
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(vector1, vector2)
    cosine_sim = similarity_matrix[0][0]
    
    return cosine_sim