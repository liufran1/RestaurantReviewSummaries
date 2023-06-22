from bs4 import BeautifulSoup
import requests
import time
import unicodedata
import re

import concurrent.futures

import pandas as pd
import openai
import os


openai_api_key = os.environ['open_api_key']
openai.api_key = openai_api_key

def get_completion(prompt, model="gpt-3.5-turbo"): 
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]



def format_prompt(cleansed_reviews):
  text_data=""
  iter=0
  for line in cleansed_reviews:
    text_data+=str(iter)+' '+line+'\n'
    iter+=1

  return f"""
  here are some reviews for a restaurant delimited by the newline character - 
  give me an overall review of the restaurant based off of them:
  ```
  {text_data}
  ```
  """


def get_reviews(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  reviews = soup.find_all("p", {"class": re.compile("^comment*")})
  return reviews

def clean_reviews(all_reviews):
  # all_reviews : list of strings
  return ([unicodedata.normalize('NFKD',re.sub(r'<p class=\"comment.* lang=\"en\">|</span></p>','',str(x))) for x in all_reviews])



def get_top_cleanreviews(url, max_page=10):
  # Just start with first page
  all_reviews=[]

  with concurrent.futures.ThreadPoolExecutor() as executor:
      urls = [url + f'?start={pagenumber}' for pagenumber in range(0, max_page, 10)]
      
      futures = [executor.submit(get_reviews, url) for url in urls]
      
      for future in concurrent.futures.as_completed(futures):
          next_reviews = future.result()
          all_reviews += next_reviews

  cleansed_reviews = clean_reviews(all_reviews)

  return cleansed_reviews

    
    

def get_all_cleanreviews(url):

  # Get all reviews
    all_reviews=get_reviews(url=url)
    next_page=True
    pagenumber=0

    while next_page:
      pagenumber+=10
      next_url = url+f'?start={pagenumber}'
      print(next_url)
      next_reviews=get_reviews(next_url)
      
      if len(next_reviews)>0:
        all_reviews+=next_reviews
      else:
        next_page=False

    from sklearn.feature_extraction.text import TfidfVectorizer

    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans


    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(cleansed_reviews)

    true_k=20

    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=200, n_init=10)
    model.fit(X)


    labels=model.labels_
    clusters=pd.DataFrame(list(zip(cleansed_reviews,labels)),columns=['title','cluster'])

    return
    # do kmeans clustering here