from aws_utils.dynamo_helper import DynamoDb
import os
import json
import uuid

DYNAMO_DB_TABLE = os.environ["dynamo_db_table"]
PARTION_KEY = os.environ["dynamo_table_partition_key"]
SORT_KEY = os.environ["dynamo_table_sort_key"]

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

    def validate_data(self, body):
        empty_keys = [k for k, v in body.items() if v == '']
        if empty_keys:
            return empty_keys
        else:
            return True

    def prepare_data(self, body, application_type):
        """
        Adds PARTITION key and SORT key to the body of schema delivered
        """
        template_to_add_keys = {
                PARTION_KEY: str(uuid.uuid1()),
                SORT_KEY: application_type
            }
        # merge body and new keys
        body.update(template_to_add_keys)
        flag = self.validate_data(body)
        if isinstance(flag, bool):
            return body
        else:
            return flag


    def producer_processor(self):
        """
        1. prepare data to be sent to dynamodb with uuid and application_type
        2. load data to dynamodb for schema of event type of producers
        """
        body, application_type = self.parse_event()
        data = self.prepare_data(body, application_type)
        if isinstance(data, dict):
            dynamod_db_object = DynamoDb(table_name=DYNAMO_DB_TABLE, data=data)
            dynamod_db_object.load_data_to_dynamo_table()
            return True
        else:
            return data