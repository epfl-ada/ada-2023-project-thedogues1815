# Thedogues1815 project folder

## Wiki and wacky Covid news
The goal of this project is to showcase the link between Wikipedia and the spread of Fake news, conspiracy theories, and general misinformation on COVID-19. Are there existing links? Does one influence the other? Let's see!
## Abstract: 
Wikipedia, while increasingly vigilant against fake news, is a primary information source for many. During the pandemic, several outlandish theories gained traction. Can we link sudden upticks in Wikipedia page views to the spread of such news? Were users who believed in these theories fact-checking or amplifying? Understanding this could reveal Wikipedia's role in debunking or perpetuating conspiracy narratives. Based on the MM-COVID database of real and fake news and tweets published during 2020, we aim first to classify the themes of the claims/theories that were most reported as fake. Then, thanks to the Coronawiki dataset and the Wikimedia REST API, we will link these with the pageview count of the related Wikipedia pages during the different phases of COVID-19. The first axis of our analysis will be temporal (e.i. we see the evolution in time during 2020). The second axis is the language, we analyze the difference in traction of fake news and theories between English, French, and Italian.

## 1) Research questions:
- What are the themes of fake news and theories related to COVID-19 on Wikipedia? what is their traction during the months of the pandemic?
- Is there a difference between these Wikipedia views and those of the most popular non-covid related theories?  
- Is there an increase in fake news publication during COVID-19? What is the percentage of fake vs. real news on the subject for each language?
- What are the principal themes of fake news that emerged during COVID-19? are these common to the theories found on Wikipedia?
  
For the next step of our project:
- Are the themes of conspiracy theories common between languages? and do they gain more or less traction in certain languages?
- Does the source of the news have an influence? (e.g. if fake news are born from Twitter, does the related mobile Wikipedia app spike?)
- Do people fact-check or believe these fake news?

## 2) Additional dataset:
**About the MM-COVID-19 dataset**: "To help better combat the COVID-19 fake news, we propose a new fake news detection dataset MM-COVID(Multilingual and Multidimensional COVID-19 Fake News Data Repository). This dataset provides the multilingual fake news and the relevant social context. We collect 3981 pieces of fake news content and 7192 trustworthy information from English, Spanish, Portuguese, Hindi, French, and Italian, 6 different languages." 
- [MM-COVID 19 paper](https://arxiv.org/abs/2011.04088)
- [MM-COVID 19 dataset](https://github.com/bigheiniu/MM-COVID)

Paper: Yichuan Li, Bohan Jiang, Kai Shu, and Huan Liu. 2020. MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation. arXiv:2011.04088 [cs.SI].

## 3) Methods:
- *Data processing:* Filtering the MM-Covid dataset to keep only the columns of interest.
- *Data wrangling and clustering:* Creation of the conspiracy theories datasets from Wikipedia (one Covid-related and one non-Covid-related) and clustering them into subgroups.
- *News category clustering:* using the subgroups from the previous point to categorize the news in the MM-covid dataset with the same classes.
- *Wikipedia query:* Through the Wikipedia API we obtain the pageviews of the categories/pages of interest.
- *Qualitative analysis:* an examination of the content of fake news articles or tweets from the MM-COVID dataset after clustering. Investigation of the time-evolution of pageview counts for each set of theories/fake news. Empirical analysis to see if there is a difference between languages for the fake news dataset.
  
For the next steps of our project:
- *Enrichment of current analysis* by analyzing more languages and more news.
- *Quantitative analysis:* statistical tests (difference in differences, correlation test).

## 4) Organization of the tasks:
- 17-24 Nov: Automating the process of clustering MM-covid dataset based on the categories of the conspiracy theories dataset.
- 24 Nov-8 Dec: 1) Collecting all the final data and completing the plots.
  
                2) Beginning the data story website. 
- 8 Dec- 15 Dec: Finding and performing relevant statistical analysis on our data.
- 15-23 Dec: Finalizing the data story and the relevant plots. Cleaning the notebooks.

## 5) In this repo:
- Functions folder with all the external functions called in the notebook.
- Data folder with all the datasets.
- P2 notebook with our analysis.

**Papers from which we inspired ourselves from:** 
- Baptista, J.P.; Gradim, A. Understanding Fake News Consumption: A Review. Soc. Sci. 2020, 9, 185. https://doi.org/10.3390/socsci9100185
- [Can online attention signals help fact-checkers fact-check?](https://arxiv.org/abs/2109.09322)
- [Code and data for: "Can online attention signals help fact-checkers fact-check?"](https://github.com/epfl-dlab/fact-checkers-fact-check/tree/main)


