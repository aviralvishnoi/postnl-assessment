import boto3
from botocore.exceptions import ClientError

sqs_client = boto3.client("sqs")
class SQS:

    def __init__(self, queue_url) -> None:
        self.queue_url = queue_url

    def delete_message_from_queue(self, receipt_handle):
        try:
            response = sqs_client.delete_message(
                ReceiptHandle=receipt_handle,
                QueueUrl=self.queue_url
            )
        except ClientError as e:
            return str(e)
        return response