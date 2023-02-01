import json
import boto3
import datetime

client = boto3.client("events")


def lambda_handler(event, context):
    # Replace event bus name with your event bus arn

    response = client.put_events(
        Entries=[
            {
                "Time": datetime.datetime.now(),
                "Source": "Lambda Publish",
                "Resources": [],
                "DetailType": "EB Demo",
                "Detail": json.dumps(event),
                "EventBusName": "arn:aws:events:eu-central-1:320722179933:event-bus/default",
                "TraceHeader": "testdemo",
            },
        ]
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response),
    }
