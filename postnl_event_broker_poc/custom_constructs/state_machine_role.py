from aws_cdk import aws_iam as iam
from dataclasses import dataclass
from constructs import Construct


@dataclass
class SMIamRoleProps:
    state_machine_role_name: str


class SMIamRole(Construct):
    __state_machine_role = iam.Role

    def __init__(self, scope: Construct, construct_id: str, props: SMIamRoleProps):
        super().__init__(scope, construct_id)
        SMIamRole.__state_machine_role = self.create_iam_role(props)

    @property
    def get_state_machine_role(self):
        return SMIamRole.__state_machine_role

    @property
    def get_state_machine_role_arn(self):
        return SMIamRole.__state_machine_role.role_arn

    def create_iam_role(self, props):
        state_machine_role = iam.Role(
            self,
            "StateMachineIamRole",
            role_name=f"{props.state_machine_role_name}",
            assumed_by=iam.ServicePrincipal("states.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ],
        )

        return state_machine_role
