#!/usr/bin/env python
# coding: utf-8

# In[129]:


##Introduction
##Henderson, Brinlee
##DA 320
##
## In this Notebook, I seek to constrast how superhero movies perform in Metacritic scores versus all movies. I hypothesize  
## that in recent years, superhero movie ratings have outpaced those of regular movies due to the pop cultural resurgence of
## Marvel movies. 

## My central question is this: Does the increase in popularity of the superhero movies lead to an increase in 
## Metacritic scores?

## 1. Superhero Metacritic Scores vs All Metacritic Scores
## 2. Avg Superhero scores by year, by MPAA Rating
## 3. Trends in Movie Scores


##(Bonus: Metacritic Score of Spider-Man)


# In[130]:


### Gathering connection credentials
import json
##Open credentials file
with open(r'C:\Users\Bunglee\Desktop\assignments\assignments spring 2022\DA 320\credentials.json') as file:
    data = json.load(file)
    mongo_conn_str = data['mongodb']


# In[131]:


## Connecting to the database
import pymongo
import dns

client = pymongo.MongoClient(mongo_conn_str)
db = client.admin

##Gathering data
##Finding the correct database, collection
db = client["movies"]

import pandas as pd
import numpy
###Reading database data from MongoDB

movies = pd.DataFrame(list(db['metacritic'].find()))
superhero = pd.DataFrame(list(db['imdb superhero'].find()))

##Movies: Metacritic movies
##Superhero: superhero movies


# In[132]:


## Gathering Metacritic scores of superhero movies
movies.rename(columns = {'title': 'Title'}, inplace = True)

## Merge superhero titles with meta titles that match the superhero titles to produce meta scores of only superhero movies
meta_superhero = pd.merge(movies, superhero, how='inner', on = 'Title')


# In[133]:


import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, FuncFormatter
##Superhero Metacritic Scores vs All Metacritic Scores

##All movies

##Add year column
movies['year'] = pd.DatetimeIndex(movies['release_date']).year
##Group by year
by_year_all = movies.groupby(movies.year)
##Create df with avg score for each year for all movies
avg_scores_all = by_year_all.mean('score')
##Ranges from 2000 to 2020 initially. Therefore we drop last row, 2020, because superhero does not have 2020 (seen below)
avg_scores_all = avg_scores_all.drop(avg_scores_all.index[-1])
avg_scores_all['year'] = avg_scores_all.index


##Superhero movies

##Add year column
meta_superhero['year'] = pd.DatetimeIndex(meta_superhero['release_date']).year
##Group by year
by_year_sh = meta_superhero.groupby(meta_superhero.year)
##Create df with avg score for each year for all movies
avg_scores_sh = by_year_sh.mean('score')
##Ranges from 2000 to 2019
avg_scores_sh['year'] = avg_scores_sh.index



fig = plt.figure()
ax = plt.axes()

##Plotting and formatting plot
plt.title("Superhero Scores vs All Movie Scores")
plt.xlabel("Avg score")
plt.ylabel("Year")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.plot(avg_scores_all['year'], avg_scores_all['score'], c = 'black')
plt.plot(avg_scores_sh['year'], avg_scores_sh['score'], c = 'red')
plt.legend(['All', 'Superhero'], loc='upper center')


##Conclusion from Graph 1, Superhero Scores vs All Movie Scores
'''From this plot, it appears that while movie scores as a whole have been rising, superhero movies have been less 
consistent but still rising overall. Superhero movies have experienced many ups and downs and have not revealed a strong, 
clear trend. We will look deeper into why this could be the case, starting with separating by MPAA Ratings, as perhaps those
made for adults are ranking higher or lower than those with a family-oriented audience. 
'''


# In[149]:


import pylab

## Avg Superhero scores by Rating

##Group by year
by_year_rating_sh = meta_superhero.groupby(['year', 'MPAARating']).mean()
by_year_rating_sh = by_year_rating_sh.reset_index()


by_year_rating_sh_R = by_year_rating_sh[by_year_rating_sh["MPAARating"] == "R"]
by_year_rating_sh_PG13 = by_year_rating_sh[by_year_rating_sh["MPAARating"] == "PG-13"]

##Preparing plot labels and plot
plt.xlabel("Avg score")
plt.ylabel("Year")
plt.title("Superhero Movie Scores by Rating")
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))

##Plotting score changes between R rating and PG-13 ratings by year
plt.plot(by_year_rating_sh_R['year'], by_year_rating_sh_R['score'], c = 'black')
plt.plot(by_year_rating_sh_PG13['year'], by_year_rating_sh_PG13['score'], c = '#ff0000')
plt.legend(['R', 'PG-13'], loc='upper center')








## Conclusion from Graph 2, Superhero Movie Scores by Rating
'''From this plot, we can deduce that while PG-13 ratings have seen little in a noticable trend, R rated superhero movies
have increasingly received better ratings from 2000 to 2019 with the exception being a decline from 2017 to 2019.
Additionally, the mean of these scores do not coincide in any given year aside from 2005 and 2008.
Therefore, we can conclude that much of the variation in scores is due to the ratings'''


# In[135]:


## Trends in Movie Scores


#Calculate trendlines for each: Superhero R, Superhero PG13, and All Movies
z_R = numpy.polyfit(by_year_rating_sh_R['year'], by_year_rating_sh_R['score'], 1)
p_R = numpy.poly1d(z_R)

z_PG13 = numpy.polyfit(by_year_rating_sh_PG13['year'], by_year_rating_sh_PG13['score'], 1)
p_PG13 = numpy.poly1d(z_PG13)

z_all = numpy.polyfit(avg_scores_all['year'], avg_scores_all['score'], 1)
p_all = numpy.poly1d(z_all)




##Trendline calculation source: https://widu.tumblr.com/post/43624347354/matplotlib-trendline

##Setting up plot
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.xlabel("Avg score")
plt.ylabel("Year")
plt.title("Trends in Movie Scores")

## Plotting ###

##SH Dark red R
plt.plot(by_year_rating_sh_R['year'],p_R(by_year_rating_sh_R['year']), c = '#9c1919')

##SH red PG13
plt.plot(by_year_rating_sh_PG13['year'],p_PG13(by_year_rating_sh_PG13['year']), c = '#ff0000')

##All black
plt.plot(avg_scores_all['year'],p_all(avg_scores_all['year']), c = '#1f1e1e')



##Labeling lines
plt.legend(['Superhero R', 'Superhero PG-13', 'All'], loc='upper center')

##Conclusion from Graph 3: Trends in Movie scores
'''From the graph, it becomes clear that the score increase in R superhero movies outpaces that of PG-13 superhero movies.
Notably, though, most popular Marvel and DC movies are rated PG-13. Therefore, it can be determined that the Marvel movies, 
most of which are PG-13, although popular, are not ranking notably high. The score increase in R rated superhero movies 
outpaces that of all movies whereas the score increase in PG-13 superhero movies is less than that of all movies.'''


# In[136]:


## Full conclusion
'''From the datasets provided, Superhero and all Metacritic movies, we have seen that the pop culture resurgence
in Marvel and DC movies has not necessarily led to an overall increase in Metacritic scores for this genre. The trends
can be broken up into three groups: Superhero rated R movies, Superhero rated PG movies, and all movies. 


Most people would say that the Spider-Man movies in the early 2000s are better than those in recent years. In contrast to 
the percieved quality increase that led to the new popularity of Marvel and DC superhero movies in recent years, R rated
superhero movies increase in rating faster than PG-13 rated superhero movies since 2000. On average, too,  in current years,
R rated superhero movies rank higher. Therefore, although Marvel and DC movies are popular, they are not necessarily of 
higher quality, according to Metacritic, than other types of movies, both of all genres and R rated
superhero movies.'''


# In[146]:


##Bonus: Metacritic Scores of Spider-Man Movies

#Plot set up
plt.gca().xaxis.set_major_formatter(FormatStrFormatter('%.0f'))
plt.xlabel("Year")
plt.ylabel("Score")
plt.title("Change in Metacritic Scores of Spider-Man Movies")

#Data: Spider-Man movies
meta_superhero_spider = meta_superhero[meta_superhero['Title'].str.contains('Spider-Man')]
plt.plot(meta_superhero_spider['year'], meta_superhero_spider['score'], c = 'red')

##Spider-Man movie scores are only just now beginning to score similarly to those in the early 2000s

##The 2018 outlier is Intro the Spiderverse, which Sony produced, not Disney's Marvel.


# In[ ]:




