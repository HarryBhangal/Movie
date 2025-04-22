import pandas as pd
import numpy as np
import ast # convert genre data into list format

# 1) Data preprocessing
movie= pd.read_csv(r'C:\Project\tmdb_5000_movies.csv')
credit= pd.read_csv(r'C:\Project\tmdb_5000_credits.csv')

merged= pd.merge(movie, credit,on= 'title')

#columns to be used for predictions
merged = merged[['title', 'cast', 'crew', 'overview', 'keywords', 'genres']]

merged.dropna(inplace=True)

def convert(obj): # converts data into list form
    l=[]
    for i in ast.literal_eval(obj) :
        l.append(i['name'])
    return l
merged['genres'] = merged['genres'].apply(convert)
merged['keywords'] = merged['keywords'].apply(convert)

def convert2(obj): #picks top 3 artist
    l=[]
    counter=0
    for i in ast.literal_eval(obj) :
        if counter!=3:
         l.append(i['name'])
         counter+=1
        else:
           break 
    return l

merged['cast']=merged['cast'].apply(convert2)

def fetch_director(obj): # picks director
    l=[]
    for i in ast.literal_eval(obj) :
        if i['job']=='Director':
           l.append(i['name'])
           break
    return l

merged['crew']= merged['crew'].apply(fetch_director)

merged['overview']=merged['overview'].apply(lambda x:x.split()) # to convert string into list 

# removing whitespace using replace and lambda
merged['genres'] = merged['genres'].apply(lambda x:[i.replace(" ","") for i in x])
merged['keywords'] = merged['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
merged['cast'] = merged['cast'].apply(lambda x:[i.replace(" ","") for i in x])
merged['crew'] = merged['crew'].apply(lambda x:[i.replace(" ","") for i in x])

merged['tags']= merged['genres']+merged['keywords']+merged['cast']+merged['crew']+merged['overview']

new_df= merged[['title', 'tags']]# new dataframe

new_df['tags']=new_df['tags'].apply(lambda x: " ".join(x))# convert tags to string 
new_df['tags']=new_df['tags'].apply(lambda x: x.lower())# convert tags to lower case

# 2) Vectorization 
from sklearn.feature_extraction.text import CountVectorizer 
cv= CountVectorizer(max_features=6000, stop_words='english')
vector= cv.fit_transform(new_df['tags']).toarray()

import nltk # to remove similar words like love loving into one word 
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
   y=[]
   for i in text.split():
      y.append(ps.stem(i))
      return " ".join(y)
new_df['tags']= new_df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity# finding smallest distance btw vectors
similarity= cosine_similarity(vector)

# Main reccomndation

def recommend(movie):
   movie_index = new_df[new_df['title']=='movie'].index[0]
   distances= similarity[movie_index]
   movie_list= sorted(list(enumerate(similarity[0])), reverse=True,keys= lambda x:x[1])[1:6] # to sort and fetch top 5 similar movies to this

   for i in movie_list:
      print(new_df.iloc[i[0]].title)


import pickle #move data from this file to app file
pickle.dump(new_df, open('movie.pkl', 'wb'))
pickle.dump(similarity,open('similarity.pkl','wb'))