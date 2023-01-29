import json
from producer_logic import ProducerLogic


def lambda_handler(event, context):
    producer_logic_object = ProducerLogic(event)
    flag =producer_logic_object.producer_processor()
    if isinstance(flag, bool):
        response = {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": "Hello, World!"}'
        }
    else:
        response = {
            "statusCode": 422,
            "headers": {"Content-Type": "application/json"},
            "body": '{"message": "These keys '+ json.dumps(flag) + ' don\'t have a correct value"}'
        }
    return response
