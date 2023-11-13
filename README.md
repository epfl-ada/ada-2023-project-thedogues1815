# Thedogues1815 project folder

## Wiki and wacky Covid news
The goal of this project is to showcase the link between Wikipedia page visits and the spread of Fake news. Are there existing links?
## Abstract: 
Wikipedia, while increasingly vigilant against fake news, is a primary information source for many. During the pandemic, several outlandish theories gained traction. Can we link sudden upticks in Wikipedia page views to the spread of such news? Were users who believed in these theories fact-checking or amplifying? Understanding this could reveal Wikipedia's role in debunking or perpetuating conspiracy narratives. Based on the MM-COVID database of real and fake news and tweets published during 2020, we aim to classify the themes of the claims that were most reported as fake. Then, thanks to the Coronawiki dataset and the Wikimedia REST API, we will link these with the pageview count of the related Wikipedia pages. The first axis of our analysis will be temporal (e.i. we see the evolution in time during 2020). The second axis is the language, we analyse the difference in traction of fake news between English, French, and Italian. 

## 1) Research questions:
- Is there an increase in fake news publication during COVID? and did people stay interested in fake news after the lockdown?
- What are the principal themes of fake news that emerged during COVID?
- What are the principal themes that interest people?
- Are the themes common between languages? and do they gain more or less traction?
- Does the source of the news have an influence? (e.g. if fake news are born from Twitter, does the related mobile Wikipedia app spike?)
- Do people fact-check or believe these fake news?


## 2) Additional dataset:
**About the MM-COVID 19 dataset**: "To help better combat the COVID-19 fake news, we propose a new fake news detection dataset MM-COVID(Multilingual and Multidimensional COVID-19 Fake News Data Repository). This dataset provides the multilingual fake news and the relevant social context. We collect 3981 pieces of fake news content and 7192 trustworthy information from English, Spanish, Portuguese, Hindi, French and Italian, 6 different languages." 
- [MM-COVID 19 paper](https://arxiv.org/abs/2011.04088)
- [MM-COVID 19 dataset](https://github.com/bigheiniu/MM-COVID)

Paper: Yichuan Li, Bohan Jiang, Kai Shu, and Huan Liu. 2020. MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation. arXiv:2011.04088 [cs.SI].

## 3) Methods:
- Data processing: Filtering the MM-Covid dataset to keep only the columns of interest.
- News category clustering: 
- Wikipedia query: Through the Wikipedia API we obtain the pageviews of the categories/pages of interest.
- Qualitative analysis: examination of the content of fake news articles or tweets from the MM-COVID dataset after clustering. Investigation of the major source of fake news (web news, Twitter). Empirical analysis to see if there is a difference between languages.
- Quantitative analysis: statistical tests ???

## 4) Organization of the tasks:




**About papers which we can inspire ourselves from:** 
- [Can online attention signals help fact-checkers fact-check?](https://arxiv.org/abs/2109.09322)
- [Code and data for: "Can online attention signals help fact-checkers fact-check?"](https://github.com/epfl-dlab/fact-checkers-fact-check/tree/main)


