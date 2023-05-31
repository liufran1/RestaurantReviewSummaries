import restuarantsummarize
import re
import random

from flask import Flask, request
app = Flask(  # Create a flask app
	__name__,
)


@app.route('/reviews', methods=['GET'])
def get_summary():
  pattern = re.compile("^.*yelp.com\/biz.*$")
  
  input_url = request.args.get('input_url')
  if input_url is None:
    return 'Input a valid url', 400
  if not pattern.match(input_url):
    return 'Input a yelp website', 400
  

  
  cleansed_reviews = restuarantsummarize.get_top_cleanreviews(input_url)
  prompt = restuarantsummarize.format_prompt(cleansed_reviews)
  
  result = restuarantsummarize.get_completion(prompt)
  return f"review summary for {input_url}: {result}", 200


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)

