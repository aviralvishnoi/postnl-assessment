from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from utils.environment import MyEnv
from custom_constructs.api_gateway import ApiGateway, ApiGatewayProps
from custom_constructs.lambda_function import LambdaFunction, LambdaProps
from custom_constructs.iam_role import IamRole, IamRoleProps
from custom_constructs.dynamodb import DynamoDbTable, DynamoDbTableProps
from custom_constructs.step_function import StepFunction, StepFunctionProps

class PostnlEventBrokerPocStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        deploy_environment = MyEnv.DEV.value

        """
        Step 1. Create Dynamodb table
        """
        dynamodb_table_name = self.node.try_get_context("dev")["dynamodb_table_name"]
        dynamodb_table_partition_key = self.node.try_get_context("dev")["table_partition_key"]
        dynamodb_table_sort_key = self.node.try_get_context("dev")["table_sort_key"]
        dynamodb_table = DynamoDbTable(
            self,
            "dynamoDbTableId",
            DynamoDbTableProps(
                dynamodb_table_name=dynamodb_table_name,
                dynamodb_table_partition_key_col_name=dynamodb_table_partition_key,
                dynamodb_table_sort_key_col_name=dynamodb_table_sort_key,
            ),
        )

        """
        Step 2. Create IAM Role for Lambda Function
        """
        iam_role_name = (
            "iamrole_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        lambda_iam_role = IamRole(
            self,
            "lambdaIamRole",
            IamRoleProps(iam_role_name),
        )

        """
        Step 3. Create producer lambda function to integrate with api gateway
        """
        lambda_function_name = (
            "lambda_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        lambda_environment_variables = {
                "dynamo_db_table": dynamodb_table_name,
                "dynamo_table_partition_key": dynamodb_table_partition_key,
                "dynamo_table_sort_key": dynamodb_table_sort_key
            }
        lambda_id = "EBProducerLambda"
        lambda_code_base = "src/producer_lambda"
        eb_producer_lambda = LambdaFunction(
            self,
            "EBProducerLambda",
            LambdaProps(
                lambda_function_name,
                lambda_iam_role.get_lambda_role,
                lambda_environment_variables,
                lambda_code_base,
                lambda_id
            ),
        )

        """
        Step 4. Create api gateway to get details of producers to create publish events
        """
        rest_api_name = (
            "restapi_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        usage_plan_name = (
            "usage_plan_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        eb_api_gateway = ApiGateway(
            self,
            "EBApiGatway",
            ApiGatewayProps(
                deploy_environment,
                rest_api_name,
                usage_plan_name,
                eb_producer_lambda.get_lambda_function,
            ),
        )
        """
        Step 5 : Grant Lambda Permission to read/write to DynamoDB table
        """
        dynamodb_table.get_dynamodb_table.grant_read_write_data(
            eb_producer_lambda.get_lambda_function
        )
        """
        Step 6 : Create step function to deploy producer stack
        """
        state_machine_name = (
            "state_machine_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        eb_step_function = StepFunction(
            self,
            "EBStepFunction",
            StepFunctionProps(
                state_machine_name
            )
        )