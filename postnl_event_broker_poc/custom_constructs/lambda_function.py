from aws_cdk import aws_lambda as lambda_function, aws_iam as iam
from dataclasses import dataclass
from constructs import Construct


@dataclass
class LambdaProps:
    lambda_name: str
    lambda_iam_role: iam.Role
    lambda_environment_variables: object
    lambda_code_base: str
    lambda_id: str


class LambdaFunction(Construct):
    __lambda_function = lambda_function.Function

    def __init__(self, scope: Construct, id: str, props: LambdaProps) -> None:
        super().__init__(scope, id)
        LambdaFunction.__lambda_function = self.create_lambda_function(props)

    @property
    def get_lambda_function(self):
        return LambdaFunction.__lambda_function


    def create_lambda_function(self, props):
        hello_lambda = lambda_function.Function(
            self,
            id=f"{props.lambda_id}",
            function_name=f"{props.lambda_name}",
            runtime=lambda_function.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_function.Code.from_asset(f"{props.lambda_code_base}"),
            role=props.lambda_iam_role,
            environment=props.lambda_environment_variables
        )
        return hello_lambda
