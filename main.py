import random, string

import restuarantsummarize

from flask import Flask, render_template, request
app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

ok_chars = string.ascii_letters + string.digits
@app.route('/')  # What happens when the user visits the site
def base_page():
	random_num = random.randint(1, 100000)  # Sets the random number
	return render_template(
		'base.html',  # Template file path, starting from the templates folder. 
		random_number=random_num  # Sets the variable random_number in the template
	)
@app.route('/2')
def page_2():
	rand_ammnt = random.randint(10, 100)
	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
	return render_template('site_2.html', random_str=random_str)

# @app.route('/reviews')
@app.route('/reviews', methods=['GET'])
def get_summary():
  input_url = request.args.get('input_url')
  if input_url is None:
    return 'Missing input_url parameter', 400
  
  cleansed_reviews = restuarantsummarize.get_top_cleanreviews(input_url)
  prompt = restuarantsummarize.format_prompt(cleansed_reviews)
  
  result = restuarantsummarize.get_completion(prompt)
  # result = input_url
  # return result, 200
  return f"review summary for {input_url}: {result}", 200


if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # EStablishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)

