from aws_cdk import (
    aws_dynamodb as dynamodb,
)

from constructs import Construct
from dataclasses import dataclass

@dataclass
class DynamoDbTableProps:
    dynamodb_table_name: str
    dynamodb_table_partition_key_col_name: str
    dynamodb_table_sort_key_col_name: str


class DynamoDbTable(Construct):
    __dynamodb_table = dynamodb.Table

    def __init__(self, scope: Construct, id: str,props: DynamoDbTableProps):
        super().__init__(scope, id)
        DynamoDbTable.__dynamodb_table = self.create_dynamodb_table(props)
    

    @property
    def get_dynamodb_table(self):
        return DynamoDbTable.__dynamodb_table

    def create_dynamodb_table(self,props):
        return dynamodb.Table(
            self,
            "dynamoDbTableId",
            table_name=props.dynamodb_table_name,
            encryption=dynamodb.TableEncryption.AWS_MANAGED,
            partition_key=dynamodb.Attribute(
                name=props.dynamodb_table_partition_key_col_name,
                type=dynamodb.AttributeType.STRING
                ),
            sort_key=dynamodb.Attribute(
                name=props.dynamodb_table_sort_key_col_name,
                type=dynamodb.AttributeType.STRING
            )
        )