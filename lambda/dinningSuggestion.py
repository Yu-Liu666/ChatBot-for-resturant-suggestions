import boto3
import json
import logging
import os


def lambda_handler(event, context):
    # TODO implement
    # intent_name = event['currentIntent']['name']
    # if intent_name == 'DiningSuggestionsIntent':
    slots = event['currentIntent']['slots']
    message = "City: " + slots["Location"] + "," + "Cuisine: " + slots["Cuisine"] + ", \n" + "Time: " + slots[
        "time"] + ", \n" + "Number of people: " + slots["NumberOfPeople"] + ", \n" + "Phone Number: " + slots[
                  "PhoneNumber"] + "."
    store_message = slots["Location"] + "," + slots["Cuisine"] + "," + slots["time"] + "," + slots[
        "NumberOfPeople"] + "," + slots["PhoneNumber"]

    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-west-2.amazonaws.com/181838262582/orders'
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=store_message
    )
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "SSML",
                "content": "You’re all set. You provide following information: \n" + message + "\nExpect my recommendations shortly! Have a good day.",
            },
        }
    }