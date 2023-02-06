from aws_cdk import aws_stepfunctions as sfn, aws_iam as _iam
from constructs import Construct
from dataclasses import dataclass


@dataclass
class StepFunctionProps:
    state_machine_name: str
    state_machine_role: str
    state_definition_json: dict


class StepFunction(Construct):
    def __init__(self, scope: "Construct", id: str, props) -> None:
        super().__init__(scope, id)
        StepFunction.__eb_stepfunction = self.create_state_machine_from_json_definition(
            props
        )

    @property
    def get_state_machine_arn(self):
        return StepFunction.__eb_stepfunction.attr_arn

    def create_state_machine_from_json_definition(self, props):
        eb_state_machine = sfn.CfnStateMachine(
            self,
            id="EBDeployInfraStateMachine",
            role_arn=props.state_machine_role,
            definition=props.state_definition_json,
            state_machine_name=props.state_machine_name,
        )

        return eb_state_machine
