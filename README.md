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
- What topics were different languages most interested in?
- Which languages shared the most in common during their coverage of Fake News during the COVID crisis? Is there any significant difference?
- How "unique" and specialized was the coverage of each language

## Dataset construction, methodology, analysis
**N.B:** In parts I and II, we focus on English Wikipedia, we then expand our scope to multiple languages in part III. 

### **Datasets construction:** 

0. *Aggregated_timeseries:* We use this dataset to identify the main trends across Wikipedia and to differentiate the relative increase of our studied web pages against the rest.
    - *Used in part I & II*
1. *Conspiracy_dataset:* We parsed the links on the Wikipedia [template conspiracy theory page](https://en.wikipedia.org/wiki/Template:Conspiracy_theories), which unify links to all pages related to fake news and conspiracy theories across time. It gives us a representative look at global fake news and conspiracy theory attention on Wikipedia during the lockdown. 
    - *Used in part I, II, III*
2. *COVID_misinformation:* For fake news more oriented towards COVID, we parsed the [COVID-19 misinformation page](https://en.wikipedia.org/wiki/COVID-19_misinformation) and extracted the articles referenced inside of each paragraph, and associated them with their original part title, and paragraph subtitle to later apply the bag of word method for news classification. 
    - *Used in part II*
3. *News_dataset_cl:* This dataset is used to introduce a link between Wikipedia viewcounts and media attention on various misinformation subjects. It comes from the paper [MM-COVID: A Multilingual and Multimodal Data Repository for Combating COVID-19 Disinformation](https://arxiv.org/abs/2011.04088) which provides a multilingual fake news dataset, their claim, and the publishing dates of articles.
    - *Used in part I & II*
4. *Interventions:* This dataset contains the dates of different important mobiity restriction phases for different countries. We use it to study the effects of mobility restrictions on Fake News interest
    - *Used in part III*
5. *Multi_lang_COVID_misinformation:* We apply the function developed for the COVID_misinformation dataset to parse wikipedia pages (extraction of links and the section to which they belong) and apply it to COVID misinformation pages in [French](https://fr.wikipedia.org/wiki/D%C3%A9sinformation_sur_la_pand%C3%A9mie_de_Covid-19#D%C3%A9sinformation_des_gouvernements_et_dirigeants), [Italian](https://it.wikipedia.org/wiki/Disinformazione_sul_SARS-CoV-2), Spanish, Arab, German, Portuguese, Russian, and Chinese. We then translated all the part titles and subtitles and used the Wikipedia API to identify the English version of the articles referenced in the other language pages. This allows us to create a common ground to compare the overlap of referenced articles across languages and to study common -and different- interests in COVID-19 Fake News across multiple languages.

### **Methodology & Analysis:**
#### Nota Bene.
Many technical details (like curve smoothing, correlation calculation...) are glossed over here. You are welcome to go view our notebooks to understand more about  our work!

#### **Part I**: Was COVID a hot topic during lockdown?
- *Datasets used:* Aggregated_timeseries & Conspiracy_dataset & Covid_misinformation

*Goal:* Identify a methodology to extract articles related to COVID-19 misinformation. Progressive zoom in the Wikipedia COVID fake news and theories landscape: Assess how relevant fake news and theories were, and more in-depth about Covid related Fake News.

*Method:* 
- *Preprocessing:*
    - We perform feature analysis on the *Covid_misinformation* dataset to remove irrelevant articles with heavy cofounders (eg. Donald Trump ect) or no close relationship to the topic.

- *Action 1.1:* 
    - We are curious about the increase in interest in Fake news as a whole on Wikipedia. To investigate this, we compare the relative increase of pageviews in pages before and during the first COVID lockdown period (March 2020 to May 2020). We evaluate the statistical significance of this increase using the **Difference-in-Difference** method   
- *Action 1.2:*
    - We plot **pie charts** to visualize the evolution of the most popular Fake News article types before, during and after the COVID lockdown
- *Action 1.3:* A similar analysis to 1.1 was conducted to show that the group of articles from the *COVID-misinformation* dataset also had a statistically significant increase.
- *Action 1.4*   
    - For a deeper, topical look at the COVID-19 related misinformation, we group the retained articles from the preprocessing and their views along the selected main categories defined in the Wikipedia [COVID-19 misinformation](https://en.wikipedia.org/wiki/COVID-19_misinformation#Vaccines). Our Fake News Topics now are: 
        - Virus origin
        - Incidence and mortality
        - Disease spread
        - Prevention
        - Vaccines
        - Treatment
    - Based on this, we do a topic based D-in-D to see the relative increase of each topic with regards to the global trend.
  
#### **Part II**: Wikipedia as a vigilante against misinformation
- *Datasets used:* Covid_misinformation & News_dataset_cl
- *Goal:* Study the overlap between COVID misinformation in Wikipedia and web-published fake news. Then try to identify the relationship between media attention towards COVID-related fake news and Wikipedia article attention. With this, we build a timeline of user interest towards various topics and see how restrictions in mobility affect the types of misinformation that are circulated.

*Method:* 
- *Action 2.1:*
    - We classify the news articles from the *News_dataset_cl* into the 6 categories defined in *Action 1.4*. For this we use bags of words built using the various headings and paragraph titles found in the COVID-19 misinformation page. (Note that a piece of news can be classified into more than one category). 
- *Action 2.3:*
    - We plot the evolution of the aggregated pageviews from the various articles parsed from the COVID-19 misinformation set **vs** daily fake news publications from the News_dataset_cl. We then evaluate the [Spearman's Rank Correlation Coefficiant](https://en.wikipedia.org/wiki/Spearman%27s_rank_correlation_coefficient) to evaluate the correlation between both curves (pre maximum and post maximum).
- *Action 2.4:*
    - Having prooved that the viewcount of the COVID-19 misinformation dataset is a good topical and behavioural match to "naturally occuring" Fake News publications related to COVID-19, we try to establish a storyline of Fake news interest during the different phases of the pandemic between January and July 2020. (wikipedia )
    - We study the speed of viewcount increase (that we call *Virality*) and the percentage of viewcount increase (which we call *Popularity*) for each article, both with regards to the global wikipedia norm. 
    - We also consider their relationship with mobility changepoints

#### **Part III**: Multilingual analysis of COVID-19 misinformation
- *Datasets used:* Multi_lang_COVID_misinformation
- *Goal:* Study the relationship between COVID Wikipedia pages for different languages. Since the Wikipedia pages in different languages don't have the same structure (so we cannot compare main headings), we want to analyse the links they refer to. What kind of overlap is there between each language?

*Method:* 
- *Action 3.1:*
    - We build word clouds for each of the considered COVID-19 misinformation languages. They are built using the titles of the referenced articles. We can then see what topics each language mostly focused on.
    - Note 
- *Action 3.2:*
    - Comparative histogram between languages to show the constitution of links that they point towards. What percentage is common with other languages, what percentage only exists in the original language, what percentage exists in english
- *Action 3.3:*
    - In order to quantify better the relationship between languages, we look at the Jaccard similarity of BOWs built for each language out of the titles of parsed articles which were found to have an english equivalent.
- *Action 3.4:*
    - We construct a chord plot with the thickness of the chords tying two languages proportional to the count of shared articles between languages.



