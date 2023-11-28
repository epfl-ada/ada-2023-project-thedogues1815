# Thedogues1815 project folder

## Wiki's Wacky Covid News
The goal of this project is to showcase the link between Wikipedia and the spread of Fake news, conspiracy theories, and general misinformation on COVID-19. Are there existing links? Does one influence the other? Let's see!
# Abstract: 
Wikipedia, while increasingly vigilant against fake news, is a primary information source for many. During the pandemic, several outlandish theories gained traction. Can we link sudden upticks in Wikipedia page views to the spread of such news? Were users who believed in these theories fact-checking or amplifying? Understanding this could reveal Wikipedia's role in debunking or perpetuating conspiracy narratives. Based on Wikipedia's pageview count (Coronawiki dataset and the Wikimedia REST API), we explore the main conspiracy theories and fake news (used for benchmarking). We analyse the main theories on COVID-19, specifically, and study their pageview count through the months of the pandemic. Then, based on the MM-COVID database of real and fake news and tweets published during 2020, we aim at linking the main topics witth the count from the related wikipedia articles. For this, first we classify the news in main categories common to those defined for wikipedia. The first axis of our analysis will be temporal (e.i. we see the evolution in time during 2020). The second axis is the language, we analyze the difference in traction of fake news and theories between English, French, and Italian.

# Research questions:
**1) Wiki fake news**
 - What are the main fake news on Wikipedia and how do their traction avolve during the pandemic?
   
**2) Wiki COVID-19 misinformation**
 - What are the themes of fake news and theories related to COVID-19 on Wikipedia? What is their traction during the months of the pandemic?
 - Is there a difference between these Wikipedia views and those of the most popular non-covid related theories?
   
**3) COVID-19 fake vs real news**
 - Is there an increase in fake news publication during COVID-19? What is the percentage of fake vs. real news on the subject for each language?
 - What are the principal themes of fake news that emerged during COVID-19? are these common to the theories found on Wikipedia?
 - How do the views of the themes of fake news in wikipedia compare with the surge in publication of the news? do the peak dates match?
  
For the next step of our project:

**Language analysis**: Are the themes of conspiracy theories common between languages? and do they gain more or less traction in certain languages?

**Mobility analysis**: During decreased mobility periods, was there a bigger increase of visits to fake news related topics relative to all other wiki articles, or simply historically with regards to fake news articles? How did conspiracy theories about COVID emerge throughout lockdown phases, and is Wikipedia a good tool to track down their respective growth? (Here compare with the fake news dataset).

**Statistical analysis**: Is the correlation statistically relevant? Is there a causal relationship between Wikipedia and the publication of fake news?

**Open questions**: Does the source of the news have an influence? (e.g. if fake news are born from Twitter, does the related mobile Wikipedia app spike?) Do people fact-check or believe these fake news?

# Additional dataset:
**About the MM-COVID-19 dataset**: "To help better combat the COVID-19 fake news, we propose a new fake news detection dataset MM-COVID(Multilingual and Multidimensional COVID-19 Fake News Data Repository). This dataset provides the multilingual fake news and the relevant social context. We collect 3981 pieces of fake news content and 7192 trustworthy information from English, Spanish, Portuguese, Hindi, French, and Italian, 6 different languages." 
- [MM-COVID 19 paper](https://arxiv.org/abs/2011.04088)
- [MM-COVID 19 dataset](https://github.com/bigheiniu/MM-COVID)

Paper: Yichuan Li, Bohan Jiang, Kai Shu, and Huan Liu. 2020. MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation. arXiv:2011.04088 [cs.SI].

# Methods:
- *Data processing:* Filtering the MM-Covid dataset to keep only the columns of interest.
- *Data wrangling and clustering:* Creation of the conspiracy theories datasets from Wikipedia (one Covid-related and one non-Covid-related) and clustering them into subgroups.
- *News category clustering:* using the subgroups from the previous point to categorize the news in the MM-covid dataset with the same classes.
- *Wikipedia query:* Through the Wikipedia API we obtain the pageviews of the categories/pages of interest.
- *Qualitative analysis:* an examination of the content of fake news articles or tweets from the MM-COVID dataset after clustering. Investigation of the time-evolution of pageview counts for each set of theories/fake news. Empirical analysis to see if there is a difference between languages for the fake news dataset.
  
For the next steps of our project:
- *Enrichment of current analysis* by analyzing more languages and more news and comparing with the 
- *Quantitative analysis:* statistical tests (difference in differences, correlation test).

# Organization of the tasks:
- **17-24 Nov:** Automating the process of clustering MM-covid dataset based on the categories of the conspiracy theories dataset.
- **24 Nov-8 Dec:** 1) Collecting all the final data about mobility and completing the missing plots for the different languages.
                2) Beginning the data story website. 
- **8 Dec-15 Dec:** Finding and performing relevant statistical analysis on our data.
- **15-23 Dec:** Finalizing the data story and the relevant plots. Cleaning the notebooks.

# In this repo:
- Functions folder with all the external functions called in the notebook.
- Data folder with all the datasets.
- P2 notebook with our analysis.

**Papers from which we inspired ourselves from:** 
- Baptista, J.P.; Gradim, A. Understanding Fake News Consumption: A Review. Soc. Sci. 2020, 9, 185. https://doi.org/10.3390/socsci9100185
- [Can online attention signals help fact-checkers fact-check?](https://arxiv.org/abs/2109.09322)
- [Code and data for: "Can online attention signals help fact-checkers fact-check?"](https://github.com/epfl-dlab/fact-checkers-fact-check/tree/main)


