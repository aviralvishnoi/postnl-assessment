import json
from consumer_logic import ConsumerLogic


def lambda_handler(event, context):
    consumer_logic_object = ConsumerLogic(event)
    flag = consumer_logic_object.consumer_processor()
    if isinstance(flag, bool):
        response = {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": "Subscription Registered Successfully!"}'
        }
    else:
        response = {
            "statusCode": 422,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": '+ json.dumps(flag) + '}'
        }
    return response
