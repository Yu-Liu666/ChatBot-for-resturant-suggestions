import boto3
import json
import logging
import os


def lambda_handler(event, context):
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
              "contentType": "SSML",
              "content": "Hi there, how can I help?"
            },
        }
    }

