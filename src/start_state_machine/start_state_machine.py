import os
import json
import boto3
import logging
from sqs_helper import SQS

logger = logging.getLogger()
logging.getLogger().setLevel(logging.DEBUG)
SQS_URL = os.environ["sqs_queue_url"]
sfn_client = boto3.client('stepfunctions')

def extract_record(event):
    return event["Records"][0]

def prepare_pay_load(record):
    body = record["body"]
    return body

def get_receipt_handle(record):
    receipt_handle = record["receiptHandle"]
    return receipt_handle

def delete_message_from_queue(receipt_handle):
    sqs_object = SQS(SQS_URL)
    sqs_object.delete_message_from_queue(receipt_handle)

def start_state_machine(state_machine_arn, event):
    record = extract_record(event)
    payload = prepare_pay_load(record)
    receipt_handle = get_receipt_handle(record)
    response = sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=payload
    )
    logging.debug(response)
    deletion_response = delete_message_from_queue(receipt_handle)
    if isinstance(deletion_response, str):
        logger.error(deletion_response)
    
    return response