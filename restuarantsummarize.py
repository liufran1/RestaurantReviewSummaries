from bs4 import BeautifulSoup
import requests
import time
import unicodedata
import re

import concurrent.futures

import pandas as pd
import openai



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


# def clean_reviews(all_reviews):
#   # all_reviews : list of strings
#   return ([unicodedata.normalize('NFKD',str(x)
#                   .replace('<p class="comment__09f24__D0cxf css-qgunke"><span class="raw__09f24__T4Ezm" lang="en">','')
#                   .replace('</span></p>','')) 
#                   for x in all_reviews])
  
#   # <p class=\"comment.* lang=\"en\">

def get_top_cleanreviews(url, max_page=30):
  # Just start with first 3 pages
  all_reviews=[]

  with concurrent.futures.ThreadPoolExecutor() as executor:
      urls = [url + f'?start={pagenumber}' for pagenumber in range(0, max_page, 10)]
      
      futures = [executor.submit(get_reviews, url) for url in urls]
      
      for future in concurrent.futures.as_completed(futures):
          next_reviews = future.result()
          all_reviews += next_reviews

  cleansed_reviews = clean_reviews(all_reviews)

  return cleansed_reviews

  



  # for pagenumber in range(10, 50, 10):
  #   next_url = url+f'?start={pagenumber}'
  #   next_reviews=get_reviews(next_url)
  #   all_reviews+=next_reviews
    
    
    

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

    # do kmeans clustering here