import json
import random
import restuarantsummarize
import re


def lambda_handler(event, context):
    pattern = re.compile("^.*yelp.com\/biz.*$")

    try:
        input_url = event['queryStringParameters']['input_url']
    except:
        return {
                'statusCode': 200,
                'body': json.dumps('API available')
            } 

    if input_url is None:    
        return {
                'statusCode': 200,
                'body': json.dumps('Input a valid url')
            }
    try: 
        if pattern.match(input_url):
            cleansed_reviews = restuarantsummarize.get_top_yelp_cleanreviews(restuarantsummarize.clean_url(input_url))
        else:  
            cleansed_reviews = restuarantsummarize.get_reviews(restuarantsummarize.clean_url(input_url))
    except:
        return {
                'statusCode': 400,
                'body': json.dumps('Whoops there was a problem getting reviews from site')
            }

    
    prompt = restuarantsummarize.format_prompt(cleansed_reviews)
    
    try:
        result = restuarantsummarize.get_completion(prompt)
        return {
                'statusCode': 200,
                'body': json.dumps(f"review summary for {input_url}: {result}")
            }
    except:
        return {
                'statusCode': 400,
                'body': json.dumps('Looks like there was a problem getting the computer to summarize these reviews')
            }
