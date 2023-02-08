import boto3
import json
from botocore.exceptions import ClientError
sqs_client = boto3.client("sqs")

class SQS:
    def __init__(self, queue_url) -> None:
        self.queue_url = queue_url

    def generate_group_id(self, message_body):
        group_id = (
            message_body["consumer_application_name"]
            + message_body["consumer_name"]
            + message_body["consumer_business_unit"]
            + message_body["type_of_endpoint"]
            + message_body["subscription_type"]
        )
        return group_id

    def send_message_to_queue(self, message_body):
        try:
            response = sqs_client.send_message(
                QueueUrl = self.queue_url,
                MessageBody = json.dumps(message_body) if isinstance(message_body, dict) else message_body,
                MessageGroupId = self.generate_group_id(message_body),
                # MessageDeduplicationId = 
            )
        except ClientError as e:
            return str(e)

        return response