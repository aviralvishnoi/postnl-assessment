from aws_cdk import aws_iam as iam
from dataclasses import dataclass
from constructs import Construct


@dataclass
class SMIamRoleProps:
    lambda_role_name: str
    eb_sqs_arn: str
    eb_state_machine_arn: str


class SMIamRole(Construct):
    __lambda_role = iam.Role

    def __init__(self, scope: Construct, construct_id: str, props: SMIamRoleProps):
        super().__init__(scope, construct_id)
        SMIamRole.__lambda_role = self.create_iam_role(props)

    @property
    def get_lambda_role(self):
        return SMIamRole.__lambda_role

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
                            "sqs:ReceiveMessage",
                            "sqs:GetQueueAttributes",
                            "sqs:GetQueueUrl",
                            "sqs:ListQueues",
                            "sqs:DeleteMessage"
                        ],
                        resources=[
                            f"{props.eb_sqs_arn}",
                        ]
                    ),
                    iam.PolicyStatement(
                        actions=[
                            "states:StartExecution"
                        ],
                        resources=[
                            f"{props.eb_state_machine_arn}"
                        ]

                    )
                ]
            )
        )
        return lambda_iam_role
