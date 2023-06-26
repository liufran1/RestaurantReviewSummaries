Manual deployment

Create lambda layer image:
* `docker build --platform=linux/amd64 --no-cache --tag get_reviews .`

In container:
* `pip install RestaurantReviewSummaries/src/ -t python/`
* `zip -r get_reviews_lambda.zip .`

In local:
* `docker cp <container_id>:/var/task/get_reviews_lambda.zip .`

On AWS: 
* upload zip to s3
* add new version of existing layer
* update function to use new version
* copy lambda code if necessary

**To Do**:

* Build front end that makes the API call
  * Probably can't get time under 10 seconds - set up progress bar animation that progresses based on steps

**Improvements**:
* Handle additional 500 scenarios
  * Bad URLs
  * too much text on resulting page
  * no reviews on resulting page
* Automate deployment steps
* Generalize to any site that has reviews - (prompt chaining)[https://learn.deeplearning.ai/chatgpt-building-system/]
  * reading the raw html is too many tokens
  * get all tags that contain text. pass tag and example to ChatGPT to identify what elements to pull all of 
* Parallelize website scraping when retrieving all reviews
* Add in clustering to functions
* refine text clustering method 
  * This currently incorporates very rudimentary text clustering https://towardsdatascience.com/how-to-easily-cluster-textual-data-in-python-ab27040b07d8
* Do search from front end
  * https://docs.developer.yelp.com/reference/v3_business_search
