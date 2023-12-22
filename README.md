# Thedogues1815 project folder -> [Our datastory](https://bottinel.github.io/TheDoguesDataStory/)

## # Wiki's Wacky Covid Factory
The goal of this project is to showcase the link between Wikipedia and the spread of Fake news, conspiracy theories, and general misinformation on COVID-19, and to study their contents in different languages. 

Why is this relevant?
Can Wikipedia viewcounts be used as a marker to identify fake news trends?
Which languages gossiped together? 
What's the data story behind the game of gossip and finger-pointing that went down during the COVID-19 lockdown phase? 

Let's find out!

## Abstract: 
The COVID-19 lockdown was a really weird moment in time, and while real-world human activities came to a halt, our online presence only grew [[1]](https://www.sciencedirect.com/science/article/pii/S2210670721004637). 

And with great web time, comes great (wacky) **Fake News**.

So, during a period where people spent much of their time online, and searched for information online, many turned to Wikipedia, one of the world's biggest information providers, and it saw its traffic greatly increase [[2]](https://arxiv.org/pdf/2005.08505.pdf).

Whether it was used by users as a resource to fact-check their data, or a way to go deeper down the rabbit hole doesn’t matter, it tells us a story about Fake News. Their emergence patterns, their relative importance in different languages...

We want to evaluate the usefulness of Wikipedia as a tool for studying misinformation across multiple languages and use it as a way to explore online users' relationship with COVID-related fake news during limited mobility periods.

## Research questions: 

1. **Was COVID a hot topic during lockdown?**
- During the period of interest (lockdown of 2020), compared with other years, is there a statistically significant increase in views for pages related to fake news compared to other articles in Wikipedia?
- If that is the case, can we differentiate the increase in fake news interest from the general increase in traffic to Wikipedia during the lockdown period?
- And what about Covid-related misinformation?

2. **Wikipedia as a tool to study misinformation**
- What is the relationship between fake news published on the web during the COVID lockdown and articles labelled as linked with COVID-19 misinformation on wikipedia? Is Wikipedia attention a good representation fo global media attention?
- Can we identify a storyline of interest towards different Fake News topics? How is the evolution of interest related to restricted mobility periods? Is Wikipedia a better tool to do this than currently existing web news datasets?

3. **Covid fake news around the world**
- Which languages shared the most in common during their coverage of Fake News during the COVID crisis? What topics were they most interested in?
- How does our past analysis now look like if we consider different languages?

## Dataset construction, methodology, analysis
**N.B:** In parts I and II, we focus on English Wikipedia, we then expand our scope to multiple languages in part III. 

### **Datasets construction:** 

0. *Aggregated_timeseries:* We use this dataset to identify the main trends across Wikipedia and to differentiate the relative increase of our studied web pages against the rest.
    - *Used in part I & II*
1. *Conspiracy_dataset:* We parsed the links on the Wikipedia [template conspiracy theory page](https://en.wikipedia.org/wiki/Template:Conspiracy_theories), which unify links to all pages related to fake news and conspiracy theories across time. It gives us a representative look at global fake news and conspiracy theory attention on Wikipedia during the lockdown. 
    - *Used in part I, II, III*
2. *COVID_misinformation:* For fake news more oriented towards COVID, we parsed the [COVID-19 misinformation page](https://en.wikipedia.org/wiki/COVID-19_misinformation) and extracted the article links from each paragraph, and associated them with their original part title, and paragraph subtitle to later apply the bag of word method for news classification. 
    - *Used in part II*
3. *News_dataset_cl:* This dataset is used to introduce a link between Wikipedia viewcounts and media attention on various misinformation subjects. It comes from the paper [MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation](https://arxiv.org/abs/2011.04088) which provides a multilingual fake news dataset, their claim, and the publishing dates of articles.
    - *Used in part I & II*
4. *Mobility_2020-2022:* We used the mobility time series to extract the important mobility restriction periods. We can then use this to identify the link between the different phases of mobility restrictions and use this for the difference in differences method.
    - *Used in part III*
5. *Multi_lang_COVID_misinformation:* We apply the function and preprocessing developed for the COVID_misinformation part and apply it to COVID misinformation pages in French, Italian, Spanish, Arab, German, Portuguese, Russian, and Chinese. We then translated all the part titles and subtitles and used the Wikipedia API to identify the English version of the articles referenced in the other language pages. This allows us to create a common ground to compare the overlap of referenced articles across languages and to study interest in COVID-19 Fake News across multiple languages.


### **Methodology & Analysis:**

#### **Part I**: Was COVID a hot topic during lockdown?
- *Datasets used:* Aggregated_timeseries & Conspiracy_dataset

*Goal:* Identify a methodology to extract articles related to COVID-19 misinformation. Progressive zoom in the Wikipedia COVID fake news and theories landscape: Assess how relevant fake news and theories were, and more in-depth about Covid fake news, and then about the main categories of fake news.

*Method:* 
- *Action 1.1:* 
    - Clean the COVID_misinformation dataset as some articles have too many cofounders due to the high traffic that they drive and their relationship to many misinformation subjects at once (eg. Donald Trump, Steve Bannon...), and others cannot directly be shown to be COVID related (eg. Chinese Communist Party).
    - As such, we performed feature analysis, hand labeling articles that we deemed relevant (high spike in attention, low attention pre-lockdown, higher attention after lockdown), and those that we deemed irrelevant.
    - This allowed for an efficient selection of articles directly related to Fake news topics based on [Skewness](https://en.wikipedia.org/wiki/Skewness), Max Views, and the [Kurtosis metric](https://en.wikipedia.org/wiki/Kurtosis) (see the relevant part in the notebook for more contextual information on metrics).

- **QUESTIONS ABOUT THIS PART -> HOW WAS THE DATA AGGREGATED**
- *Action 1.2:* 
    - We are curious about the increase of interest in Fake news as a whole on Wikipedia. For this, we compare the relative increase of pages after and during the first COVID lockdown period (march 2020 to May 2020) by analysing the evolution of interest in fake news article that can't be explained by the increase use of wikipedia by applying the difference in difference method. (e.i ....)

- *Action 1.3* 
    - After seeing a significant increase of 50 % for fake news we went more in-depth and evaluated the relative increase in COVID-19 related fake news. To do that we use the COVID-19 misinformation dataset and applied the difference and difference method to compare the increase in COVID-19 related fake news with the increase in overall wikipedia views.

*Analysis:* 
- We find that there is an important rise in attention towards fake news during the lockdown. From the linear regression, between the control group (containing the views of the articles before lockdown) and the treatment group (containing the views of article during the lockdown), we obtain : R-squared =  0.692, P-value = 0.00, and a coefficient = 0.4819. This indicates that around a 50% increase in attention towards fake news that the rise in general Wikipedia usage that can't be explained by the null hypothesis.

- Furthermore, the rise in attention towards COVID-related fake news is even more substantial with an  R-squared = 0.470, P-value = 0.00, and coefficient = 0.9986. This indicates that there is around a 100% increase in attention towards COVID-19 conspiracy articles.

  This allows us to prove that we can extract articles directly related to COVID-19 misinformation subjects and that they are identifiable through Wikipedia page views. We can also cluster them based on more general topics thanks to the titles and subtitles, which allows us to do further analysis.
#### **Part II**: Wikipedia as a vigilante against misinformation
- *Datasets used:* Covid_misinformation & News_dataset_cl
- *Goal:* Study the overlap between COVID misinformation in Wikipedia and web-published fake news. Then we try to identify the relationship between media attention towards COVID-related fake news and Wikipedia article attention. With this, we can build a timeline of user interest towards various topics and see how restrictions in mobility affect the types of misinformation that are circulated.

*Method:* 
- *Action 1.1:*
    - We group articles and their views along the selected main categories defined in the Wikipedia [COVID-19 misinformation](https://en.wikipedia.org/wiki/COVID-19_misinformation#Vaccines) categories (based on the article's main headings). Our Fake News Topics are: 
        - Virus origin
        - Incidence and mortality
        - Disease spread
        - Prevention
        - Vaccines
        - Treatment
    - From there, we use the subtitles and sub-subtitles of each main category from the wikipedia article to build a bag of words (bow) to classify the web news dataset. With this, we have a bag of words for each main heading which represents the topics covered. (Note: recurrent words which were not representative of each category were removed -> eg. COVID-19, country names...)

- *Action 1.2:*
    - We introduce the news_dataset from [MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation](https://arxiv.org/abs/2011.04088). As we are currently studying the english version of the [COVID-19 misinformation](https://en.wikipedia.org/wiki/COVID-19_misinformation#Vaccines) article, we focus on the english based language Fake News. This dataset gives us access to 2168 individual pieces of media content which have been labelled as Fake.
     - Using the BoW created in *Action 1.2*, we then classify the selected news articles into the 6 categories. A piece of news is classified as belonging to a Fake News topic if the claim (short description of the piece of news) contains words from the BoW. (note that a piece of news can be classified into more than one category)
     - Based on this, we can see that 84% of the topics covered by the Fake news dataset are represented in the topics covered by the wikipedia article.

- *Action 1.3:*
    - We plot a weighted average of the viewcount from   

- *Action 1.4:*
    - We then plot the timeline of published news along with the view count of the corresponding Wikipedia articles per main category and try to infer a correlation between them. 
  
*Analysis:* 
    - Following our bow analysis, we mana


#### **Part III**: COVID fake news around the world
- *Datasets used:* Multi_lang_COVID_msinforamtion
- *Goal:* Study the relationship between COVID Wikipedia pages for different languages. Since the Wikipedia pages in different languages don't have the same structure (so we cannot compare main headings), the only thing we can analyse is the links they refer to.

*Method:* 
- *Action 1.1:* To see the similarities in Wikipedia articles across different languages, we can create a pseudo-bag of words for the titles of the Wikipedia pages about COVID-19 parsed from the Multi_lang_COVID_msinforamtion. We clean the links, separating the words and removing stopwords and words that are over present, and then we count the number of unique words, along with their number frequency to create word clouds for each language.
  
- *Action 1.2:* In order to quantify better the relationship between languages, we can construct a chord plot with the thickness of the chords tying two languages that is proportional to the overlap of words between the two languages. We then calculate the Jaccard similarity between pairs of languages to quantify this finding. 



