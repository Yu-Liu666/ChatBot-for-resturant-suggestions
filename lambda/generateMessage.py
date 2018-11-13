import json
import requests
import boto3
def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    response = client.post_text(
        botName='chatbot',
        botAlias='Prod',
        userId='sss',
        sessionAttributes={
            'string': ''
        },
        requestAttributes={
            'string': ''
        },
        inputText=event["messages"][0]['unstructured']['text']
    )
    # url = "https://us-west-2.console.aws.amazon.com/lex/api/lexruntimetext"
    return {
        "statesCode": 200,
        "body": {
            "messages": [
                {
                  "type": 0,
                  "unstructured": {
                    # "id": content["id"],
                    "text": response['message']
                    # "timestamp": content["timestamp"]
                  }
                }
            ]
        }
    }