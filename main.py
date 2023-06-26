import restuarantsummarize
import re
import random

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(  # Create a flask app
	__name__,
)

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["10 per minute"] # Based on OpenAI limit of 40,000 Tokens per Minute
)

@app.route('/')
def index():
    return 'Franklin\'s app server is running', 200

@app.route('/reviews', methods=['GET'])
def get_summary():
  pattern = re.compile("^.*yelp.com\/biz.*$")
  
  input_url = restuarantsummarize.clean_url(request.args.get('input_url'))
  
  if input_url is None:
    return 'Input a valid url', 400
  if pattern.match(input_url):
    cleansed_reviews = restuarantsummarize.get_top_yelp_cleanreviews(input_url)    
  else:
    cleansed_reviews = restuarantsummarize.get_reviews(input_url)
  

  
  if not cleansed_reviews:
      return "Error getting reviews", 400
  prompt = restuarantsummarize.format_prompt(cleansed_reviews)

  result = restuarantsummarize.get_completion(prompt)
  if result:
    return f"review summary for {input_url}: {result}", 200
  else:
    return "Error getting summary", 400


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=8080
	)

