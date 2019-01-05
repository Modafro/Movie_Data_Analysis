
# coding: utf-8

# # Movie Data Analysis

# ## Introduction
# 
# The following work serves to analyse the data of more than 10,000 movies. The first part of this project will focus on data wrangling to clean up the data and subsequently perform an analysis with the cleaned up data. The second analysis will focus on studying different trends and correlations so that tentative conclusions can be made. Assumptions will clearly be stated and by no means are the conclusions of this work definitive but more so speculative as no rigorous statistical analysis will be performed. The project will present tentative relations between different sets of data and the reader is encouraged to use their own critical approach to these conclusions.
# 
# 1. What genre of movie is popular year to year?
#     - Has there been more votes in recent years compared to early years?
#     - Does the level of popularity change over time?
#     - Is there a relationship between vote count and popularity?
#     - Does a movie that's more popular mean a better average vote for a given movie?
# 2. How does "money" interact with various parameters?
#     - Are movies with higher budgets more popular? 
#     - Does a higher budget mean higher revenue? Does more popularity mean more revenue?
#     - Do higher budget command better ROIs? Do popular movie command better ROIs?
#     - Which movie genres have the highest/lowest budget/revenue?
#     - Which movie genres have the best "return on investment" or ROI?
#     - Impact of grouped popularity and budget on ROI?
# 3. Which production company produces the most movies?
#     - With grouped production companies, is there a correlation between average vote and popularity?
#     - With grouped production companies, is there a correlation between popularity / average vote and ROI?
#     - Which production companies have the biggest budget/ROI? 
#     - Which production companies have the best ROI?
# 4. Do certain Directors command higher budgets?
# 

# ## Data Wrangling

# The first step to any projects of this sort is to import two main libraries irrespective if they are used or not which are _numpy_ and _pandas_. Additional libraries will be added as needed.

# In[21]:


# Import numpy should we use numpy related built-in functions. np is the common abbreviation
import numpy as np

# Import pandas should we use pandas related built-in functions. pd is the common abbreviation
import pandas as pd


# For ease and convenience due to the nature of this work, the project will be imported in a Dataframe format.

# In[23]:


# Import the tmdb-movies.csv file in a pandas dataframe and read only pd

movie_data_base_df=pd.read_csv('tmdb-movies.csv')


# In[24]:


print ("The original data has a total of {} movies. One should expect this number to be reduced after the data wrangling.".format(len(movie_data_base_df)))


# The first step is to lighten the data. For the purpose of our analysis, the following data will not be utilized:
# - tagline
# - keywords
# - homepage
# - overview
# 
# The other columns that won't be needed are the __budget__ and __revenue__ columns. The assumption made is that the adjusted_budget and adjusted_revenue data that account for inflation are much more relevant for comparison purposes between different movies of different release dates. It allows comparison to be made on the _same level playing field_. This is not to say that the data deleted can't be used for meaningful analysis, it simply won't be used in this project.
# 
# The wrangling will also ascertain that there are no duplicate values in the dataframe.

# In[25]:


#Verify duplicates in Dataframe

movie_data_base_df[movie_data_base_df.duplicated(keep=False)]


# As shown in the table above, TEKKEN movie appears twice in the table so one of the two entries will be removed from the dataframe.

# In[26]:


# drop one duplicated row

movie_data_base_dfDup=movie_data_base_df.drop_duplicates(subset=['imdb_id','popularity'])                                                     


# In[27]:


# Define a function to delete unwanted columns from a given dataframe. This function will have two inputs, dataframe and a string 
#(or list of strings) of the columns to be deleted and returns a dataframe without these columns

def delete_columns(data_frame, deleted_column):
    lighter_df=data_frame.drop(deleted_column, axis=1)
    return lighter_df


# In[28]:


# Apply delete_columns function to delete unwanted columns

movie_data_base_dfLighters=delete_columns(movie_data_base_dfDup, ['budget', 'revenue','homepage','tagline','keywords','overview'])


# Next, any numerical data that has a value of 0 will entrain the row containing 0 to be deleted. The assumption is that a 0 in such data will be regarded as unreliable data and the requirement for our analysis is that we have a full picture devoid of any discrepancies. One could argue that a revenue of 0 is possible however, the assumption is that the revenue values are net values (i.e.: after all expenses are deducted) and one can reasonably assume that an absolute value of exactly 0 is highly improbable. 

# In[29]:


# Deletion of rows that have a value of zero in any columns with numbers
movie_data_base_dfLighter=movie_data_base_dfLighters[(movie_data_base_dfLighters[['runtime','budget_adj',
                                                                                  'revenue_adj']] != 0).all(axis=1)]


# Another verification that is required with such a large data is to ascertain that there are no "empty" cells. Any empty cells will be replaced by a string to ease potential error messages further into our analysis.

# In[30]:


# define a function that takes in a dataframe as argument and replace empty cells with the string "No Data"

def replace_EmptyWithNoData(data_emptycells):
    data_filledWithNoData=data_emptycells.fillna("No Data")
    return data_filledWithNoData


# In[31]:


# Apply function on latest dataframe

movie_data_base_dfClean=replace_EmptyWithNoData(movie_data_base_dfLighter)


# A few columns have pipe characters (|) such as _cast_ or _production companies_. In order for analysis to be made on these columns, we will remove these pipe characters to create a list of strings within those columns.

# In[32]:


# create a dataframe with columns that contain pipe characters.

pipe_characters_df=movie_data_base_dfClean.filter(['director','cast', 'genres','production_companies'], axis=1) 


# In[33]:


# Define a function to separate the pipe characters that takes in a string with pipe characters as an argument and 
# returns a series of string (pipe characters separated)

def split_pipe(movie_data):
    words_splited=movie_data.split("|")
    return words_splited

# write a function to apply the split_pipe function on the dataframe that contains all the columns with pipe characters:

def split_pipes(movie_datas):
    return movie_datas.applymap(split_pipe)


# In[34]:


# Apply split_pipes on pipe character dataframe

pipe_characters_dfSplit=split_pipes(pipe_characters_df)

print ("Sample of the dataframe with split characters removed:")
pipe_characters_dfSplit.head()


# As it can be observed in the above dataframe, there can be multiple strings under a given column for a given movie. To simplify the dataframe for analysis purposes, a dataframe containing one single "dominant" string, which will be the first string within a series, will be created. As an example, for id 135397,
# - the cast [Chris Pratt, Bryce Dallas Howard, Irrfan Khan...] will become [Chris Pratt] which is the first string of the list 
# - the genres [Action, Adventure, Science Fiction, Thriller] will become [Action]
# - etc.

# In[35]:


# define a function that takes a list of strings as its argument and returns the first string of that list

def dominant_value(list_value):
    return list_value[0]

# define a function to apply dominant_value to a dataframe

def dominant_values(list_values):
    return list_values.applymap(dominant_value)


# In[36]:


# Apply dominant_values on the pipe character dataframe

dominant_value_df=dominant_values(pipe_characters_dfSplit)

print ("Sample of dataframe with dominant strings only: ")
dominant_value_df.head()


# In the Introduction section, we mentioned return on investment or ROI. It's a metric that measures the true value of profitability for a given movie and is defined as follows as per our assumptions:
# 
# $$ROI(\%)=\frac{profits-budget}{budget}\times100$$

# <center>where $revenue=profits-budget$</center>

# In[37]:


# define a function a function to calculate ROI

def return_investment(investment, revenue):
    ROI=revenue/investment*100
    return ROI


# In[38]:


# remove the director, cast, genres, and production companies columns from dfClean and replace them with the dominant_df columns
movie_data_base_delete=delete_columns(movie_data_base_dfClean, ['director','cast','genres','production_companies'])

# merge the latest dataframe (delete) with the dominant_df dataframe
movie_data_base_dfMerge=pd.concat([movie_data_base_delete.reset_index(drop=True), dominant_value_df.reset_index(drop=True)], axis=1)

# add ROI column to the merged dataframe
movie_data_base_dfMerge['ROI(%)']=return_investment(movie_data_base_dfMerge.loc[:,'budget_adj'], movie_data_base_dfMerge.loc[:,'revenue_adj'])

print("Sample of how the dataframe looks like thus far:")
movie_data_base_dfMerge.head()


# We previously replaced all blank values with "No Data". In the spirit of consistency based on this project's approach, any movie that has a "No Data" value will be viewed as imcomplete data and therefore not admissible for the analysis portion. 

# In[39]:


# define a function to remove rows that contain "No Data" which will take in as argument a dataframe and a string or list of
# strings as arguments and returns the dataframe without the rows containing "No Data"

def removing_NoData(nodata_df, column_head):
    for head in column_head:
        NoData_Dataframe=nodata_df[nodata_df[head].str.contains("No Data")==False]
    return NoData_Dataframe

NoData_df=removing_NoData(movie_data_base_dfMerge, ['director','cast','genres','production_companies'])


# The last phase of the data wrangling is to establish minimum values for some of the data that will be considered for our analysis. These are _personal_ preferences and not official guidelines:
# - runtime: minimum 2 min
# - vote_count: minimum 10 counts
# - budget_adj: minimum \$10,000
# 

# In[40]:


# define function a function that takes as arguments a dataframe, a string and a minimum number (integer or float) and returns 
# the dataframe containing data with values respecting the boolean setting

def set_minimum(MinData_df, Head, MinValue):
    Data_Min=MinData_df[MinData_df[Head]>MinValue]
    return Data_Min


# In[41]:


# apply set_minimum function on latest dataframe

min_runtime_df=set_minimum(NoData_df, 'runtime', 2)
min_votecount_df=set_minimum(min_runtime_df, 'vote_count',10)
min_budgetadj_df=set_minimum(min_votecount_df,'budget_adj', 10000)


# The data wrangling phase is now complete. A new meaningful name will be assigned to the final dataframe and proceed to the analysis phase of the project.

# In[42]:


#let's assign a neat dataframe name for what will be used in the analysis
movie_database_analysis_df=min_budgetadj_df

print ("Sample of the dataframe set the analysis will be done for:")
movie_database_analysis_df.head()


# In[43]:


print ("After all the data wrangling, we are left with {} movies to perform our analysis.".format(len(movie_database_analysis_df)))


# ## Data Analysis

# As a reminder, here is the list of the analysis that will be performed:
# 
# 1. What genre of movie is popular year to year?
#     - Has there been more votes in recent years compared to early years?
#     - Does the level of popularity change over time?
#     - Is there a relationship between vote count and popularity?
#     - Does a movie that's more popular mean a better average vote for a given movie?
# 2. How does "money" interact with various parameters?
#     - Are movies with higher budgets more popular? 
#     - Does a higher budget mean higher revenue? Does more popularity mean more revenue?
#     - Do higher budget command better ROIs? Do popular movie command better ROIs?
#     - Which movie genres have the highest/lowest budget/revenue?
#     - Which movie genres have the best "return on investment" or ROI?
#     - Impact of grouped popularity and budget on ROI?
# 3. Which production company produces the most movies?
#     - With grouped production companies, is there a correlation between average vote and popularity?
#     - With grouped production companies, is there a correlation between popularity / average vote and ROI?
#     - Which production companies have the biggest budget/ROI? 
#     - Which production companies have the best ROI?
# 4. Do certain Directors command higher budgets?

# ### Movie Genre Popularity in a Given Year

# What genre of movie is popular year after year?
# First, let's assess how many movies there are per genre to ascertain that there's enough data.

# In[44]:


print ("Number of movies per genre in the data:")
movie_database_analysis_df['genres'].value_counts()


# As the table above show, History, Western and especially TV Movie genres don't have a lot of data which will be acknowledged should their data be used in a tentative conclusion.

# In[45]:


# groupby the dataframe by release year and genres and take the mean of genres popularity

Groupby_YearGenre=pd.DataFrame({'mean_popularity':movie_database_analysis_df.groupby(['release_year','genres'])['popularity'].mean()}).reset_index()
print ("Sample of average popularity per genre in a given year")
Groupby_YearGenre.head()


# In[46]:


# find the max popularity mean value for a given year 
Groupby_YearGenreMax=Groupby_YearGenre.groupby(['release_year','genres']).max()


popularity_year=Groupby_YearGenreMax[Groupby_YearGenreMax['mean_popularity'] == Groupby_YearGenreMax.groupby(level=[0])['mean_popularity'].transform(max)]
print ("Sample most popular movie genre in a given year:")
popularity_year.head()


# For better visual representation, plots of the most popular movies in the 60s and in the last 10 years (2006-2015) will be plotted

# In[47]:


get_ipython().magic('pylab inline')
import matplotlib.pyplot as plt
import seaborn as sns


# In[48]:


popularity_year.iloc[0:10,:].plot(kind='bar', subplots=True, figsize=(10,5))
plt.ylabel('Average Popularity')
plt.xlabel('Release Year & Genres')
plt.title('Most Popular Movies in a Year')


# N.B.: In 1969, History movies were the most popular but this may be a hasty conclusion considering only have 17 movies in our history dataset from 1960 to 2015.

# In[49]:


popularity_year.iloc[len(popularity_year)-10:len(popularity_year),:].plot(kind='bar', subplots=True, figsize=(10,5))
plt.ylabel('Average Popularity')
plt.xlabel('Release Year & Genres')
plt.title('Most Popular Movies in a Year')


# N.B.: In 2015, Western movies were the most popular but this may be a hasty conclusion considering only have 16 movies in our adventure dataset from 1960 to 2015.

# ### Average Number of Votes Over the Years

# We will now analyse the average number of votes over the years and see if a trend can be associated with popularity. First we shall define a function to calculate the Pearson Correlation Coefficient ([click here](http://www.dummies.com/education/math/statistics/how-to-interpret-a-correlation-coefficient-r/) for more information)

# In[50]:


# define a function that takes two series as arguments and returns the correlation between the two series

def correlation(series_1, series_2):
    corr_result=series_1.corr(series_2)
    return corr_result


# In[51]:


# group data with respect to release year 

GroupMean_by_ReleaseYear=movie_database_analysis_df.groupby(['release_year'], as_index=False).mean()


# In[52]:


# apply correlation function between release year and average vote count

print ("Pearson r between release year and average vote count:")
correlation(GroupMean_by_ReleaseYear.loc[:,'release_year'], GroupMean_by_ReleaseYear.loc[:,'vote_count'])


# There is a strong correlation between when a movie was released and the number of votes it received for its rating. We will plot this correlation for better visual understanding.

# In[53]:


GroupMean_by_ReleaseYear.plot(kind='bar', figsize=(10,5), x='release_year', y='vote_count')
plt.ylabel('Average Vote Count')
plt.xlabel('Release Year')
plt.title('Average Vote Count Over Time')


# Looking at the graph, we can see that it's really in the last ~20 years that a sharp spark in vote counts vs release years can clearly be seen. The only data available that may explain this trend (mind you, this is based on my assumption) could be due to increased popularity of movies over the years and thus more vote count? Let's explore that theory.

# ### Level of Popularity Over Time

# In[54]:


# apply correlation function between average popularity and release year

print ("Pearson r between popularity and release year:")
correlation(GroupMean_by_ReleaseYear.loc[:,'popularity'], GroupMean_by_ReleaseYear.loc[:,'release_year'])


# The correlation in this case is weak but it is there, the level of popularity for movies tend to increase over time. I would speculate, beyond the scope of available analysis that other reasons may be that tmdb.com istself did not become a prevalent go to for movie amateurs until recently. So maybe people started voting on tmdb when they joined tmdb which would have been in 2008 when tmdb was created. Aslo the demographic most likely to join tmdb are on the younger side of things and maybe wouldn't want to necessarily watch a movie from the 60s? Take myself for example, I've been a member of imdb (not tmdb...) for 12 years now and have over 1000 votes for various tv shows and movies, most of them starting from the 80s. I don't really watch movies that are before the 80s simply because I don't want to! So maybe many millenials and generation Zs might feel the same way?
# 
# Also a young individual in their 20s during the 60s that would've watched the "popular" movies from back then would be in their 60s/70s today. Would older people really bother going to tmdb and cast a vote on all the popular movies from their young days? Not so sure that they would...
# 
# Obviously, this analysis is very subjective to my views so take it with a grain of salt, but there might be some truths in all that analysis...

# One area I do expect to see strong correlation is the higher the popularity, the higher the vote count as more people would've seen it and thus potentially the higher popularity.

# ### Popularity vs Number of Votes?

# In[55]:


# apply correlation function between popularity and number of votes

print ("Pearson r between popularity and number of votes:")
correlation(movie_database_analysis_df.loc[:,'popularity'], movie_database_analysis_df.loc[:,'vote_count'])


# Very stong correlation between popularity and vote count. The higher the popularity, the higher the vote count. Here are a few popular movies from the 60s and in the last 10 years (from 2006 to 2015)

# In[56]:


print("Most popular movies from the 60s:")

movie_database_analysis_df[movie_database_analysis_df['release_year']<1970].nlargest(10, 'popularity')


# So the table above presents a few movies that were extremely popular in the 60s, and although I previously mentioned that I don't typically watch movies from that era, one of my all time favourite Bond movies starring Sean Connery, Goldfindger, is one of my all time favourite. I actually just gave it a vote on my account (9/10) as I realized that I didn't vote for it! But that's the only movie I recall having seen from that list.

# In[57]:


print ("Most popular movies from the 2006 to 2015:")

movie_database_analysis_df[movie_database_analysis_df['release_year']>=2005].nlargest(10, 'popularity')


# So the above table shows the most popular movies in the "last 10 years" and contrary to the 60s movies, I have watched all of them and casted a vote (even reviews in some cases) for all of them on IMDB. 

# ### Popularity vs Movie Rating?

# In[58]:


# apply correlation function between popularity and average vote

print ("Pearson r between popularity and movie rating:")
correlation(movie_database_analysis_df.loc[:,'popularity'], movie_database_analysis_df.loc[:,'vote_average'])


# A weak correlation between popularity and vote average so I would approach the following statement with caution: the more popular the movie the higher the average vote. 

# ## The Money Interaction

# We will now approach the analysis in terms of any potential relationships between budget, revenue, ROI, popularity, average vote, etc.

# ### Budget vs Popularity?

# In[59]:


# apply correlation function between budget and popularity?

print ("Pearson r between budget and popularity:")
correlation(movie_database_analysis_df.loc[:,'budget_adj'], movie_database_analysis_df.loc[:, 'popularity'])


# Although it is a moderately weak correlation, one can tentatively say that the higher the budget the more popular a movie is expected to be which would make a little sense since bigger budget movies would have more money to spend on marketing.

# Let's analyse which movies tend to have the higher revenues. I would think that the more popular a movie is, the higher the revenue and also the higher the budget, the higher the revenue. Let's find out!

# ### Revenue vs Popularity and Revenue vs Budget

# In[60]:


# apply correlation function between revenue and popularity

print ("Pearson r between revenue and popularity:")
correlation(movie_database_analysis_df.loc[:,'popularity'], movie_database_analysis_df.loc[:,'revenue_adj'])


# The correlation is not as strong as I would've expected, but there's definitely a moderate strong correlation whereby, the more popular a movie, the more revenue it generates. How about budget? 

# In[61]:


# apply correlation function between revenue and budget

print ("Pearson r between revenue and budget:")
correlation(movie_database_analysis_df.loc[:,'budget_adj'], movie_database_analysis_df.loc[:,'revenue_adj'])


# Very similar result to that of popularity. So one can tentatively conclude, that the higher the budget and popularity of a 
# given movie, the higher chances there are that more revenue will be generated. However, I feel that this conclusion is a bit decieving. As a symbolic example, a movie that has a budget of \$100,000 would more easily generate a revenue of \$1,000 than say the movie that has a budget of $1,000. This is where the return on investment - ROI - allows us to compare apples to apples.

# ### ROI vs Popularity and ROI vs Budget?

# In[62]:


# apply correlation function between ROI and popularity

print ("Pearson r between ROI and popularity:")
correlation(movie_database_analysis_df.loc[:,'ROI(%)'], movie_database_analysis_df.loc[:,'popularity'])


# In[63]:


# apply correlation function between ROI and budget

print ("Pearson r between ROI and budget:")
correlation(movie_database_analysis_df.loc[:,'ROI(%)'], movie_database_analysis_df.loc[:,'budget_adj'])


# The results now are very different from the revenue standpoint, there's no correlation between popularity or budget with respect to ROI. In fact, the more money one spends on a movie doesn't necessarily mean better returns! It is also interesting to see that although no correlation exists, there is a negative sign correlation between ROI and budget...

# ### Movie Genres with Respect to Budget & Revenue

# In[64]:


# first create a datafram from grouping movie genres and get the mean of the desired metrics

GroupMean_by_Genres=movie_database_analysis_df.groupby(['genres'], as_index=False).mean().filter(['genres','budget_adj',
                                                                                                  'revenue_adj', 'ROI(%)'], axis=1 )

print ("Sample of average revenue, budget and ROI for a given genre:")  
GroupMean_by_Genres.head()


# To that table, we will add a standarized column for budget, revenue and ROI for ease of analysis.

# In[65]:


# define a function to standarize a column. takes in a column and returns the standarized value for each variable of the column

def standarize_column(column):
    return (column-column.mean())/column.std()


# In[66]:


# add standarized columns to GroupMean_by_Genres

GroupMean_by_Genres['budget_std']=standarize_column(GroupMean_by_Genres.loc[:,'budget_adj'])
GroupMean_by_Genres['revenue_std']=standarize_column(GroupMean_by_Genres.loc[:,'revenue_adj'])
GroupMean_by_Genres['ROI_std']=standarize_column(GroupMean_by_Genres.loc[:,'ROI(%)'])

print ("Sample of previous table with standarized columns:")
GroupMean_by_Genres.head()


# Based on the previous correlations explored, we know that to some extent and "with everything else being equal", the higher the budget, the higher the revenue. Let's find out the genres that command the highest budgets and the ones that command the lowest.

# In[67]:


Top_Genres_Budget=GroupMean_by_Genres.nlargest(3,'budget_adj')
Bottom_Genres_Budget=GroupMean_by_Genres.nsmallest(3,'budget_adj')

print ("Top Genres as per budget & revenue:\n")
print (Top_Genres_Budget.filter(['genres','budget_std','revenue_std']))
print ("\n\n")
print ("Bottom Genres as per budget & revenue:\n")
print (Bottom_Genres_Budget.filter(['genres','budget_std','revenue_std']))


# The Animation/Adventure genre seems to command the highest budget and revenue while the Documentary genre seems to command the exact opposite (as the standard deviation shows). Also keep in mind that we only have one movie used for TV Movie so one should not consider TV Movie in the above list for analysis. And what about the genre that commands the highest ROI? The lowest ROI?

# ### Movie Genres with Respect to ROI

# In[68]:


Top_Genres_ROI=GroupMean_by_Genres.nlargest(3,'ROI(%)')
Bottom_Genres_ROI=GroupMean_by_Genres.nsmallest(3,'ROI(%)')

print ("Top Genres as per ROI:\n")
print (Top_Genres_ROI.filter(['genres','ROI', 'ROI_std']))
print ("\n\n")
print ("Bottom Genres as per ROI:\n")
print (Bottom_Genres_ROI.filter(['genres','ROI','ROI_std']))


# As mentioned before,the TV Movie genre will not be considered due to lack of data. The action genre seems to command the highest ROI while the Science Fiction genre seems to command the lowest ROI (as the standard deviation shows) if we ignore the TV Movie genre. It is interesting to note that although Documentaries have the lowest budgets and lowest revenues, Documentaries are among the genres with the ROIs! Let's find out which Action movies have the highest ROIs and which Science Fiction movies have the worst.

# In[69]:


Action_df=movie_database_analysis_df[movie_database_analysis_df['genres'].str.contains("Action")]

print ("Top 10 movies with very high ROIs:")
Action_df.nlargest(10,'ROI(%)')


# I must admit that I'm not too familiar with many of these movies (most them being prior 1980) but I do recognize the Beverly Hill Cop Triology with the very talend Eddie Murphy. Grew up loving those movies!

# In[70]:


ScienceFiction_df=movie_database_analysis_df[movie_database_analysis_df['genres'].str.contains("Science Fiction")]

print ("Bottom 10 movies with very low ROIs:")
ScienceFiction_df.nsmallest(10,'ROI(%)')


# I haven't seen any movies on that list and contrary to the previous list, all of these movies are past 1980.

# ### Impact of Budget & Popularity on Revenue

# In[119]:


Groupby_BudgetPopularity=pd.DataFrame({'mean_revenue':movie_database_analysis_df.groupby(['original_title','popularity','budget_adj'])['revenue_adj'].mean()}).reset_index()


print ("Sample of grouped popularity & budget with respect to revenue:")
Groupby_BudgetPopularity.head()


# In[121]:


# correlation between popularity, budget and revenue

print ("Pearson r between popularity, budget and revenue:")
Groupby_BudgetPopularity.corr()

As it can be seen in the above, there is a moderately strong correlation between popularity and budget with respect to the average revenue. The higher the popularity and budget, the higher the revenue. Let's do a plot to better visual those findings.
# In[122]:


# add standarized columns

Groupby_BudgetPopularity['popularity_std']=standarize_column(Groupby_BudgetPopularity.loc[:,'popularity'])
Groupby_BudgetPopularity['budget_adj_std']=standarize_column(Groupby_BudgetPopularity.loc[:,'budget_adj'])
Groupby_BudgetPopularity['mean_revenue_std']=standarize_column(Groupby_BudgetPopularity.loc[:,'mean_revenue'])

print ("Sample of grouped popularity & budget with standarized columns:")
Groupby_BudgetPopularity.head()


# Let's now plot the relationship between these three variables in terms of standard deviation as it will be easier to fit them in the same plot.

# In[128]:


# plot the biggest revenues         
                                                        
Groupby_BudgetPopularity.nlargest(40,'mean_revenue_std').filter(['original_title','popularity_std','budget_adj_std','mean_revenue_std']).plot(x='original_title', y=['popularity_std','budget_adj_std','mean_revenue_std'], kind='bar',figsize=(20,10))
plt.ylabel('Standard Deviation Value')
plt.xlabel('Various Movies')
plt.axhline(y=0, color='black', linestyle='-', linewidth = 0.5)
plt.title('Relationship between popularity, budget with respect to biggest movie revenues')


# In[129]:


Groupby_BudgetPopularity.nsmallest(40,'mean_revenue_std').filter(['original_title','popularity_std','budget_adj_std','mean_revenue_std']).plot(x='original_title', y=['popularity_std','budget_adj_std','mean_revenue_std'], kind='bar',figsize=(20,10))
plt.ylabel('Standard Deviation Value')
plt.xlabel('Various Movies')
plt.axhline(y=0, color='black', linestyle='-', linewidth = 0.5)
plt.title('Relationship between popularity, budget with respect to smallest movie revenues')


# The two previous plot confirm the correlation. In general, if the budget and popularity standard deviations are positive (i.e.:higher than the average) it translates into higher revenues. If on the other hand, budget and popularity standard deviations are negative (i.e.: lower than the average) it translates into lower revenues.

# ## The Production Company Interaction

# Next we will do an analysis with respect to production companies which includes the number of movies made, the popularity and average rating, best ROIs etc.

# ### Number of Movies Made by Production Companies

# In[96]:


# find out the number of movies produced by production companies

production_companies_count=movie_database_analysis_df['production_companies'].value_counts()

print ("Top 10 production companies in terms of number of movies made:")
production_companies_count.iloc[0:10]


# Unsurprisingly to the movie amateur, the big producing companies are some very well knowns names such as Universal Pictures, Twentieth Century Fox Film Corp or Walt Disney Pictures. For our analysis, we will only consider production companies that have made at least 10 movies.

# In[97]:


# list of production companies that have made at least 10 movies since 1960

production_companies_10=production_companies_count[production_companies_count>=10]
production_companies_10=production_companies_10.index.values


# In[98]:


# create a dataframe of production companies with at least 10 movies

production_companies_df=movie_database_analysis_df[movie_database_analysis_df['production_companies']
                                                   .isin(production_companies_10)]


# In[99]:


# create dataframe grouped by production companies and get the mean for various metrics

Groupby_ProductionCompanies=production_companies_df.groupby(['production_companies'], as_index=False).mean().drop(['release_year','runtime',
                                                                                                   'vote_count'],1)

print ("Sample of production companies dataframe with the mean average of various metric: ")
Groupby_ProductionCompanies.head()


# In[100]:


#let's standarize the above table table

Groupby_ProductionCompanies['popularity_std']=standarize_column(Groupby_ProductionCompanies.loc[:,'popularity'])
Groupby_ProductionCompanies['vote_average_std']=standarize_column(Groupby_ProductionCompanies.loc[:,'vote_average'])
Groupby_ProductionCompanies['budget_std']=standarize_column(Groupby_ProductionCompanies.loc[:,'budget_adj'])
Groupby_ProductionCompanies['revenue_std']=standarize_column(Groupby_ProductionCompanies.loc[:,'revenue_adj'])
Groupby_ProductionCompanies['ROI_std']=standarize_column(Groupby_ProductionCompanies.loc[:,'ROI(%)'])

print ("Sample of production companies dataframe with standarized columns: ")
Groupby_ProductionCompanies.head()


# ### Popularity vs Rating with respect to Grouped Production Companies

# In[101]:


# apply correlation function between average popularity and average rating with respect to grouped production companies:

print ("Pearson r between average popularity and average rating for grouped production coompanies:")
correlation(Groupby_ProductionCompanies.loc[:,'popularity'], Groupby_ProductionCompanies.loc[:,'vote_average'])


# Remember previously we attempted to verify the correlation between popularity and average vote but there was no strong correlation. However if we group production companies and verify the same correlation, we now see that a close to strong correlation exists between average popularity and average vote. One can tentatively derive that for a given production company, the higher the average popularity the higher the average rating. Let's print some of top production companies in terms of average popularity.

# In[102]:


print("Most popular production movie companies:")

Sorted_ProductionCompanies_pop=Groupby_ProductionCompanies.sort_values(by='popularity', ascending=False).filter(['production_companies',
                                                                                                                'popularity', 'vote_average', 'popularity_std','vote_average_std'])
Sorted_ProductionCompanies_pop.head()


# From the above, we can see that Marvel Studios is very popular among movie amateurs (well above average as per the standard deviation). Let's plot those values for better visualization!

# In[103]:


#In a historgram format:

Sorted_ProductionCompanies_pop.iloc[0:10,:].plot(kind='bar', figsize=(10,5), x='production_companies', y='popularity')
plt.ylabel('Average Popularity')
plt.xlabel('Production Companies')
plt.title('Average Popularity for a Production Company')


# I recognize a few from this top 10 list, namely, Marvel Studios, Lucasfilm and Legendary Pictures. Marvel Studios seems to command movies with the highest popularity on average. I can already guess some of the movies from Marvel that are extremely popular, but let's still print them out to confirm :)

# In[104]:


Marvel_df=production_companies_df[production_companies_df['production_companies'].isin(['Marvel Studios'])]
Marvel_df


# As I anticipated, most of the latest superhero movies are found in that list and I've seen all of them!

# ### Popularity vs Revenue and Average Rating vs Revenue for Grouped Production Companies?

# In[105]:


print ("Pearson r between popularity and return on investment:")
correlation(Groupby_ProductionCompanies.loc[:,'popularity'], Groupby_ProductionCompanies.loc[:,'revenue_adj'])


# In[106]:


print ("Correlation between average vote and return on investment:")
correlation(Groupby_ProductionCompanies.loc[:,'vote_average'], Groupby_ProductionCompanies.loc[:,'revenue_adj'])


# There is a very strong correlation between average vote / popularity and revenue for a given production company. Let's plot these to have a better visualisation.

# In[107]:


Groupby_ProductionCompanies.nlargest(10,'revenue_adj').plot(x='production_companies', y=['popularity_std','vote_average_std','revenue_std'],kind='bar', figsize=(20,10))
plt.ylabel('Standard Deviation Value')
plt.xlabel('Production Companies')
plt.axhline(y=0, color='black', linestyle='-', linewidth = 0.5)
plt.title('Relationship between popularity, rating with respect to biggest movie revenues')


# In[108]:


Groupby_ProductionCompanies.nsmallest(10,'revenue_adj').plot(x='production_companies', y=['popularity_std','vote_average_std','revenue_std'],kind='bar', figsize=(20,10))
plt.ylabel('Standard Deviation Value')
plt.xlabel('Production Companies')
plt.axhline(y=0, color='black', linestyle='-', linewidth = 0.5)
plt.title('Relationship between popularity, rating with respect to smallest movie revenues')


# The two previous plot confirm the correlation. In general, if the rating and popularity standard deviations are positive (i.e.:higher than the average) it translates into higher revenues. If on the other hand, rating and popularity standard deviations are negative (i.e.: lower than the average) it translates into lower revenues.

# ### Production Companies with Respect to Budget/Revenue

# In[110]:


Top_ProductionCompanies_Budget=Groupby_ProductionCompanies.nlargest(3,'budget_adj')
Bottom_ProductionCompanies_Budget=Groupby_ProductionCompanies.nsmallest(3,'budget_adj')

print ("Top Production Companies as per budget & revenue:\n")
print (Top_ProductionCompanies_Budget.filter(['production_companies','budget_std','revenue_std']))
print ("\n\n")
print ("Bottom Production Companies as per budget & revenue:\n")
print (Bottom_ProductionCompanies_Budget.filter(['production_companies','budget_std','revenue_std']))


# We saw previously that Marvel was very popular and in line with a previous correlation exposed, Marvel movies have the biggest budgets & revenues on average!

# ### Production Companies with Repect to ROI

# In[111]:


print ("Production companies with highest ROIs:")

Sorted_ProductionCompanies_ROI=Groupby_ProductionCompanies.sort_values(by='ROI(%)', ascending=False)
Sorted_ProductionCompanies_ROI.head()


# I think it's fair to say that many will recognize the production company that leads the pack in terms of ROI. But should our reader find themselves unaware, let's display a few notable movies coming from Lucasfilm production.

# In[112]:


Lucasfilm_df=production_companies_df[production_companies_df['production_companies'].isin(['Lucasfilm'])]
Lucasfilm_df.nlargest(10,'ROI(%)')


# I think it's fair to say that our readers will have at least heard of the hugely popular Star Wars Franchise as well as Indiana Jones. 

# ## Directors that command bigger revenues

# In[113]:


Groupby_Directors=movie_database_analysis_df.groupby(['director']).mean()

print ("Sample table:")
Groupby_Directors.head()


# Directors that command the highest budget:

# In[114]:


print ("Top 10 Directors with highest revenues")
Groupby_Directors.nlargest(10, 'revenue_adj')


# ## Conclusion

# This project attempted to analyse on a limited capacity the movie data of ~4,000 movies. There were definitely some intersting trends but as mentioned throughout the project, many assumptions were made and no statistical analysis was made so the findings will remain tentative. However, readers will get a feel of some relationships that exits between different parameters such as the more popular a movie is, the more votes there will be for the rating of a given movie or that spending the big bucks on budget doesn't necessarily translate into better ratings!
# 
# There have been some limitations to this project. The adjusted budget and revenue to account for inflation is one of them. We don't know what inflation rate was used to arrive at those adjusted values. Was it an average based on inflation over the last 10 years? 20 years? 30 years? We don't know. Also we do not officially know how popularity was measured. As we've seen, over the years, the level of popularity increased but why is that? Are people watching more movies now than they did 40 years ago? Or is it the other way around? How exactly was popularity measured in 1960? 1970? Or any movies that date before 2008, the year tmdb was created. 
# 
# There many more different ways that the movie data can be analyzed but this is a good starting point for any movie amateur to aprreciate some of the tentative findings of this work!

# # References

# The following websites were used as a resource for this project:
# - stackoverflow
# - github
# 
