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

    if not pattern.match(input_url):
        return {
                'statusCode': 400,
                'body': json.dumps('Only yelp.com/biz sites currently supported. Input a yelp website')
            }
    
    cleansed_reviews = restuarantsummarize.get_top_cleanreviews(input_url)
    
    if not cleansed_reviews:
        return {
                'statusCode': 400,
                'body': json.dumps('Error pulling reviews from site')
            }

    
    prompt = restuarantsummarize.format_prompt(cleansed_reviews)

    result = restuarantsummarize.get_completion(prompt)
    if result:
        return {
                'statusCode': 200,
                'body': json.dumps(f"review summary for {input_url}: {result}")
            }
    else:
        return {
                'statusCode': 400,
                'body': json.dumps('Error getting summary')
            }

