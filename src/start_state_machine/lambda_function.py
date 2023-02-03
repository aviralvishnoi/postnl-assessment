import os
import json
import boto3
import logging
from start_state_machine import start_state_machine


STATE_MACHINE_ARN = os.environ["state_machine_arn"]


logger = logging.getLogger()
logging.getLogger().setLevel(logging.DEBUG)

def lambda_handler(event, context):
    logger.debug(event)

    response = start_state_machine(STATE_MACHINE_ARN, event)
    logger.debug(response)