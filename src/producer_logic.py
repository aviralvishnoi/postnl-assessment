from aws_utils.dynamo_helper import DynamoDb
from utils.error_response import ErrorResponse
from utils.validator import Validator
import os
import json
import uuid

DYNAMO_DB_TABLE = os.environ["dynamo_db_table"]
PARTION_KEY = os.environ["dynamo_table_partition_key"]
SORT_KEY = os.environ["dynamo_table_sort_key"]
VALID_TYPE_OF_ENDPOINT = ["HTTP"]


class ProducerLogic:
    def __init__(self, event):
        self.event = event

    def parse_event(self):
        """
        Purpose of this function is to extract body from the POST request sent by API gateway
        """
        application_type = self.event.get("path", None)
        if application_type:
            application_type = application_type[1:]

        body = self.event.get("body", None)
        if body and isinstance(body, str):
            body = json.loads(body)
        return body, application_type

    def prepare_data(self, data, application_type):
        """
        Adds PARTITION key and SORT key to the body of schema delivered
        """
        template_to_add_keys = {
            PARTION_KEY: str(uuid.uuid1()),
            SORT_KEY: application_type,
        }
        # merge body and new keys
        data.update(template_to_add_keys)
        return data

    def validate_response(self, data):
        validator_object = Validator(data, VALID_TYPE_OF_ENDPOINT)
        flag = validator_object.validate_data()
        endpoint_flag = validator_object.validate_type_of_endpoint()
        contract_flag = validator_object.validate_event_contract()

        if isinstance(flag, bool) and isinstance(endpoint_flag, bool) and contract_flag:
            return data
        else:
            error_response = {
                "INPUT_VALIDATION_FAILED": flag if isinstance(flag, bool) else False,
                "TYPE_OF_ENDPOINT_ALLOWED": endpoint_flag if isinstance(endpoint_flag, bool) else False,
                "EVENT_CONTRACT": contract_flag,
            }
            print(error_response)
            return error_response

    def producer_processor(self):
        """
        1. prepare data to be sent to dynamodb with uuid and application_type
        2. load data to dynamodb for schema of event type of producers
        """
        body, application_type = self.parse_event()
        data = self.prepare_data(body, application_type)
        print("DATA:", data)
        validated_data = self.validate_response(data)
        print(validated_data)
        
        if (
            validated_data.get("INPUT_VALIDATION_FAILED", False)
            or validated_data.get("TYPE_OF_ENDPOINT_ALLOWED", False)
            or validated_data.get("EVENT_CONTRACT", False)
        ):
            response_object = ErrorResponse(validated_data)
            return response_object.prepare_error_response(VALID_TYPE_OF_ENDPOINT)
        else:
            dynamod_db_object = DynamoDb(table_name=DYNAMO_DB_TABLE, data=data)
            dynamod_db_object.load_data_to_dynamo_table()
            return True
