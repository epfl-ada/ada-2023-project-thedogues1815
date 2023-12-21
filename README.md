# Thedogues1815 project folder -> [Our datastory](https://bottinel.github.io/TheDoguesDataStory/)

## # Wiki's Wacky Covid Factory
The goal of this project is to showcase the link between Wikipedia and the spread of Fake news, conspiracy theories, and general misinformation on COVID-19, and to study their contents in different languages. 

Can wikipedia viewcounts be used as a marker to identify fake news trends?
Which languages gossiped together? 
What's the data story behind the game of gossip and finger pointing which went down during the COVID-19 lockdown phase? 

Let's find out!

## Abstract: 
The COVID-19 lockdown was a really weird moment in time, and while real world human activities ame to a halt, our online presence only grew [[1]](https://www.sciencedirect.com/science/article/pii/S2210670721004637). 

And with great web time, come great (wacky) **Fake News**.

So, during a period where people spent much of their their time online, and searched for information online, many turned to Wikipedia, one of the world's biggest information providers, and it saw it's traffic greatly increased[[2]](https://arxiv.org/pdf/2005.08505.pdf).

Whether it was used by users as a resource to fact check their data, or a way to go deeper down the rabbit hole doesn’t matter, it tells us a story about Fake News. Their emergence patterns, their relative importance in different languages...

We want to evaluate the usefulness of Wikipedia as a tool for studying misinformation accross multiple languages, and use it as a way to explore online user's relationship with COVID related fake news during limited mobility periods.

## Research related questions: 

1. **Can we extract fake news from Wikipedia?**
During the period of interest (lockdown of 2020) with respect to the other years, is there a statistically significant increase in views for pages related to fake news compared to other articles in Wikipedia? It's interesting to investigate what this tells us about the public’s interests: can we differentiate the increase in fake news interest from the general increase in traffic to wikipedia during the lockdown period? And what about Covid-related news?

2. **Can we identify the emergence of fake news?**
We want to analyse fake news published during the covid lockdown and prove correlation between fake news publication and wikipedia pageview count increase. 
What can we observe? Which comes first? How are they related to restricted mobility periods?

3. **Covid fake news around the world**
How different are the past analysis if we consider different languages? Are there cultural differences between popular fake news or do they overlap? Finally, can we link this with country-specific mobility change points and government interventions?

## Methodology, analysis and dataset construction
**N.B:** In part I and II, we focus on english Wikipedia, we then expand our scope to multiple languages in part III. 

### **Dataset construction:** 

0. *Aggregated_timeseries:* We use this dataset to identify the main trends accross wikipedia and to differentiate the relative increase of our studied web pages against the rest.
    - *Used in part I & II*
1. *Conspiracy_dataset:* Fake We parsed the links on the Wikipedia [template conspiracy theory page](https://en.wikipedia.org/wiki/Template:Conspiracy_theories), which unites links to all pages related to fake news and conspiracy theories accross the ages. It gives us a representative look at global fake news and conspiracy theory attention on wikipedia during the time. 
    - *Used in part I*
2. *COVID_misinformation:* For fake news more oriented towards COVID, we parsed the [COVID-19 misinformation page](https://en.wikipedia.org/wiki/COVID-19_misinformation) and extracted the article links from each paragraph, and associated them with their original part title, and paragraph sub title to later apply bag of word methods. 
    - *Used in part I & II*
3. *News_dataset_cl:* This dataset is used to introduce a link between wikipedia viewcounts and media attention on various misinformation subjects. It comes from the paper [MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation](https://arxiv.org/abs/2011.04088) which provides a multilingual fake news dataset and the publishing dates of articles.
    - *Used in part II*
4. *Mobility_2020-2022:* We used the mobility time series to extract the important mobility restriction periods. We can then use this to identify the link between the different phases of mobility restrictions 
    - *Used in part II*
5. *Multi_lang_COVID_misinformation:* We apply the function and preprocessing developped for the COVID_misinformation part and apply it to COVID misinformation pages in French, Italian and Spanish. We then also translated all the part titles and subtitles, and used the wikipedia API to identify the english version of the articles referenced in the other language pages. THis allows us to create a common ground to compare the overlap of referenced articles accross languages.
    - *Used in part III*

### **Methodology & Analysis:**

#### **Part I**: Fake news on Wikipedia during the lockdown period, a useful tool?
- *Datasets used:* Aggregated_timeseries & Conspiracy_dataset

*Goal:* Assess the usability of Wikipedia as a platform for analysis of Fake News trends and emergence analysis, and identify a methodolgy to extract articles related to COVID-19 misinformation

*Method:* 
- *Action 1.1:* 
    - While all the articles from the *Conspiracy_dataset* are directly related to given Fake News, the same cannot be said from the articles parsed from the one COVID-19_msinformation dataset. 
    - Some articles are too general and have too many cofounders due to to the high traffic that they drive and their relationship to many misinformation subjects at once (eg. Donald Trump, Steve Bannon...), and others cannot directly be shown to be COVID related (eg. Chinese Communist Party). 
    - As such, we performed feature analysis, hand labeling articles which we deemed relevant (high spike in attention, low attention pre lockdown, higher attention after lockdown) and those which we deemed irrelevant.
    - This allowed for an efficient selection of articles directly related to Fake news topics based on [Skewness](https://en.wikipedia.org/wiki/Skewness), Max Views and the [Kurtosis metric](https://en.wikipedia.org/wiki/Kurtosis) (see relevant part in Data Story for more contextual information on metrics)

- **QUESTIONS ABOUT THIS PART -> HOW WAS THE DATA AGGREGATED**
- *Action 1.2:* 
    - We are wondering about the increase of interest towards Fake news as a whole on Wikipedia. For this, we compare the relative increase of pages after and during the COVID lockdown period (2020 vs 2022) by applying the difference in difference method. 
    - We use the data after the pandemic, as some relevant articles (eg. plandemic) were created during the lockdown period and did not exist before. We do this to compare the pageviews of all articles (main trend, view as baseline), general Fake news related articles, and COVID-19 related fake news. 

- *Action 1.3* 
    - We use a t-test to evaluate whether the relative increase of each part is relevant or not.

*Analysis:* 
- We find that the general attention towards Fake News could not be differentiated from the rise in attention towards wikipedia articles as a whole, which is surprising. However the rise in attention towards COVID-19 conspiracy articles was clear (which makes sense as we selected them in this way). 
- This allows us to prove that we can extract articles directly related to COVID-19 misinformation subjects, and that they are identifiable through wikipedia pageviews. We can also cluster them based on more general topics thanks to the titles and subtitles, which allows us to do further analysis.

#### **Part II**: COVID-19 misinformation, the relationship between media attention and Wikipedia pageviews
- *Datasets used:* Covid_misinformation & News_dataset_cl
- *Goal:* Identify the relationship between media attention towards COVID related fake news and wikipedia article attention. With this we can build a timeline of user interest towards various topics and see how restrictions in mobility affected the types of misinformation that circulated

*Method:* 
- *Action 1.1:*
    - We group articles and their views along the selected main categories defined in the wikipedia COVID-19 misinformation categories. They are: 
        - Virus origin
        - Incidence and mortality
        - Disease spread
        - Prevention
        - Vaccines
        - Treatment

- *Action 1.2:*
    - From there, we perform a bag of word analysis to see which key words come out often for different categories.

- *Action 1.3:* 
    - We introduce the news dataset. Using the BOW method applied from

#### **Part III**: Multilingual analysis of COVID-19 misinformation
- *Datasets used:* Multi_lang_COVID_msinforamtion

