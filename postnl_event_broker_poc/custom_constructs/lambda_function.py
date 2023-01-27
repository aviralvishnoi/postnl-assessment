from aws_cdk import aws_lambda as lambda_function, aws_iam as iam
from dataclasses import dataclass
from constructs import Construct


@dataclass
class LambdaProps:
    lambda_name: str
    lambda_iam_role: iam.Role


class LambdaFunction(Construct):
    __lambda_function = lambda_function.Function

    def __init__(self, scope: Construct, id: str, props: LambdaProps) -> None:
        super().__init__(scope, id)
        LambdaFunction.__lambda_function = self.create_lambda_function(props)

    def create_lambda_function(self, props):
        hello_lambda = lambda_function.Function(
            self,
            "EBProducerLambda",
            function_name=f"{props.lambda_name}",
            runtime=lambda_function.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=lambda_function.Code.from_asset("src"),
            role=props.lambda_iam_role,
        )
        return hello_lambda
