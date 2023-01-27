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


class PostnlEventBrokerPocStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        deploy_environment = MyEnv.DEV.value
        """
        Step 1. Create IAM Role for Lambda Function
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
        Step 2. Create producer lambda function to integrate with api gateway
        """
        lambda_function_name = (
            "lambda_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        eb_producer_lambda = LambdaFunction(
            self, "EBProducerLambda", LambdaProps(lambda_function_name, lambda_iam_role.get_lambda_role)
        )

        """
        Step x. Create api gateway to get details of producers to create publish events
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
            "restapi_"
            + self.node.try_get_context(deploy_environment)["app_name"]
            + "_"
            + self.node.try_get_context(deploy_environment)["team"]
            + "_"
            + deploy_environment
        )
        eb_api_gateway = ApiGateway(
            self, "EBApiGatway", ApiGatewayProps(deploy_environment, rest_api_name, usage_plan_name, eb_producer_lambda.get_lambda_function)
        )
