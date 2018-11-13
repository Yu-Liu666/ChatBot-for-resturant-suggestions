import boto3
import requests
import json
import logging
import os
from urllib.parse import quote

API_KEY = "IgmmjaXB8b87GrdTxFWkkN8J9gPnGMcBwQJxzRJ9QLuLrFISSgRAl3-6WfneOCTqJCpnHC4HB6SrfQb8i3OovQW" \
          "srTropH1ALLUdoeD6dcZ9WvsxNiWo3SpYyLjoW3Yx"

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Defaults for our simple example.
DEFAULT_TERM = 'dinner'
DEFAULT_LOCATION = 'San Francisco, CA'
SEARCH_LIMIT = 3


def lambda_handler(event, context):
    sqs = boto3.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName='orders')

    # Process messages by printing out body
    for message in queue.receive_messages():
        res = message.body
        break
    temp = res
    s = res.split(",")
    location = s[0]
    cuisine = s[1]
    dining_time = s[2]
    num_people = s[3]
    phone_number = s[4]
    # Number of people
    # Phone number
    result = "Hello! Here are my " + cuisine + " restaurant suggestions for " + num_people + " people, " + "at " + dining_time + ": "
    result = result + search(API_KEY, DEFAULT_TERM, location, cuisine, phone_number) + ". Enjoy your meal!"
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2',
                              endpoint_url="https://dynamodb.us-west-2.amazonaws.com")
    table = dynamodb.Table('Message')
    response = table.put_item(
        Item={
            'id': temp,
            'suggestions': result
        }
    )

    return result


def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()


def search(api_key, term, location, categories, phone_number):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'categories': categories,
        'limit': 3
    }
    s = request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)
    # return s

    res = "1. Name: " + s["businesses"][0]["name"] + "; Address: " + s["businesses"][0]["location"]["address1"] + " "
    res = res + " 2. Name: " + s["businesses"][1]["name"] + "; Address: " + s["businesses"][1]["location"][
        "address1"] + " "
    res = res + " 3. Name: " + s["businesses"][2]["name"] + "; Address: " + s["businesses"][2]["location"][
        "address1"] + " "
    client = boto3.client('sns', 'us-east-1')
    response = client.publish(
        PhoneNumber=phone_number,
        Message=res,
        # TopicArn="arn:aws:sns:us-east-1:181838262582:dynamodb"
    )
    return res