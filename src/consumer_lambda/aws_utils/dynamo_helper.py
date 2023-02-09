import boto3

dynamodb_db_resource = boto3.resource("dynamodb")

class DynamoDb:
    
    def __init__(self, table_name, data):
        self.table_name = table_name
        self.data = data

    def load_data_to_dynamo_table(self):        
        table = dynamodb_db_resource.Table(self.table_name)
        table.put_item(
            Item=self.data
        )