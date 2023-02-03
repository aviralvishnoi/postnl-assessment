from aws_cdk import Stack
from constructs import Construct
from utils.environment import MyEnv
from custom_constructs.api_gateway import ApiGateway, ApiGatewayProps
from custom_constructs.lambda_function import LambdaFunction, LambdaProps
from custom_constructs.iam_role import IamRole, IamRoleProps
from custom_constructs.dynamodb import DynamoDbTable, DynamoDbTableProps
from custom_constructs.step_function import StepFunction, StepFunctionProps
from custom_constructs.s3 import S3Bucket, S3BucketProps
from custom_constructs.sqs import SQS, SQSProps
from custom_constructs.iam_role_start_state_machine_role import (
    SMIamRole,
    SMIamRoleProps,
)
from aws_cdk.aws_lambda_event_sources import SqsEventSource


class PostnlEventBrokerPocStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        deploy_environment = MyEnv.DEV.value

        """
        Step 1. Create FIFO queu
        """
        queue_name = (
            "sqs-"
            + self.node.try_get_context(deploy_environment)["app_name"].replace(
                "_", "-"
            )
            + "-"
            + self.node.try_get_context(deploy_environment)["team"]
            + "-"
            + deploy_environment
            + ".fifo"
        )
        dead_letter_queue_name = (
            "dlq-"
            + self.node.try_get_context(deploy_environment)["app_name"].replace(
                "_", "-"
            )
            + "-"
            + self.node.try_get_context(deploy_environment)["team"]
            + "-"
            + deploy_environment
            + ".fifo"
        )
        eb_sqs_fifo = SQS(
            self, "EBProducerFifoQueue", SQSProps(queue_name, dead_letter_queue_name)
        )
        """
        Step 2. Create Dynamodb table
        """
        dynamodb_table_name = self.node.try_get_context("dev")["dynamodb_table_name"]
        dynamodb_table_partition_key = self.node.try_get_context("dev")[
            "table_partition_key"
        ]
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
        Step 3. Create IAM Role for Lambda Function
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
            IamRoleProps(iam_role_name, eb_sqs_arn=eb_sqs_fifo.get_queue_arn),
        )

        """
        Step 4. Create producer lambda function to integrate with api gateway
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
            "dynamo_table_sort_key": dynamodb_table_sort_key,
            "sqs_queue_url": eb_sqs_fifo.get_queue_url,
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
                lambda_id,
            ),
        )

        """
        Step 5. Create api gateway to get details of producers to create publish events
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
        Step 6 : Grant Lambda Permission to read/write to DynamoDB table
        """
        dynamodb_table.get_dynamodb_table.grant_read_write_data(
            eb_producer_lambda.get_lambda_function
        )
        """
        Step 7 : Create step function to deploy producer stack
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
            self, "EBStepFunction", StepFunctionProps(state_machine_name)
        )
        """
        Step 8. Create s3 bucket for artifacts
        """
        bucket_name = (
            "artifacts-s3-"
            + self.node.try_get_context(deploy_environment)["app_name"].replace(
                "_", "-"
            )
            + "-"
            + self.node.try_get_context(deploy_environment)["team"]
            + "-"
            + deploy_environment
        )
        s3_bucket = S3Bucket(self, "EBArtifactBucket", S3BucketProps(bucket_name))
        """
        Step 9. Create role for lambda function to start state machine
        """
        trigger_sm_iam_role_name = (
            "trigger_sm_iamrole_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        trigger_sm_iam_role_name = SMIamRole(
            self,
            "TriggerSMLambdaIamRole",
            SMIamRoleProps(
                trigger_sm_iam_role_name,
                eb_sqs_arn=eb_sqs_fifo.get_queue_arn,
                eb_state_machine_arn=eb_step_function.get_state_machine_arn,
            ),
        )

        """
        Step 10. Create lambda to start state machine to create infra for producer
        """
        trigger_sm_lambda_function_name = (
            "trigger_sm_lambda_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        trigger_sm_lambda_environment_variables = {
            "state_machine_arn": eb_step_function.get_state_machine_arn,
            "sqs_queue_url": eb_sqs_fifo.get_queue_url,
        }
        trigger_sm_lambda_id = "EBProducerLambdaTriggerStateMachine"
        trigger_sm_lambda_code_base = "src/start_state_machine"
        eb_producer_trigger_sm_lambda = LambdaFunction(
            self,
            "EBProducerTriggerSMLambda",
            LambdaProps(
                trigger_sm_lambda_function_name,
                trigger_sm_iam_role_name.get_lambda_role,
                trigger_sm_lambda_environment_variables,
                trigger_sm_lambda_code_base,
                trigger_sm_lambda_id,
                # source_sqs=eb_sqs_fifo.get_queue_object
            ),
        )
        eb_producer_trigger_sm_lambda.get_lambda_function.add_event_source(SqsEventSource(eb_sqs_fifo.get_queue_object, batch_size=1, report_batch_item_failures=True))
