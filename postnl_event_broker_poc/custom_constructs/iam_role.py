from aws_cdk import aws_iam as iam, aws_s3 as s3
from dataclasses import dataclass
from constructs import Construct


@dataclass
class IamRoleProps:
    lambda_role_name: str
    eb_sqs_arn: str


class IamRole(Construct):
    __lambda_role = iam.Role

    def __init__(self, scope: Construct, construct_id: str, props: IamRoleProps):
        super().__init__(scope, construct_id)
        IamRole.__lambda_role = self.create_iam_role(props)

    @property
    def get_lambda_role(self):
        return IamRole.__lambda_role

    def create_iam_role(self, props):
        lambda_iam_role = iam.Role(
            self,
            "LambdaIamRole",
            role_name=f"{props.lambda_role_name}",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole"
                )
            ],
        )

        lambda_iam_role.attach_inline_policy(
            iam.Policy(
                self,
                "CustomInlinePolicy",
                statements=[
                    iam.PolicyStatement(
                        actions=[
                            "sqs:SendMessage",
                            "sqs:GetQueueAttributes",
                            "sqs:GetQueueUrl",
                            "sqs:ListQueues"
                        ],
                        resources=[
                            f"{props.eb_sqs_arn}",
                        ]
                    )
                ]
            )
        )
        return lambda_iam_role
