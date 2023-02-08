import json
from postnl_event_broker_poc.src.consumer_lambda.consumer_logic import ConsumerLogic


def lambda_handler(event, context):
    producer_logic_object = ConsumerLogic(event)
    flag = producer_logic_object.producer_processor()
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
