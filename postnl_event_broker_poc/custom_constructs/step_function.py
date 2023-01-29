from aws_cdk import aws_stepfunctions as sfn
from constructs import Construct
from dataclasses import dataclass

@dataclass
class StepFunctionProps:
    step_function_name: str


class StepFunction(Construct):

    def __init__(self, scope: "Construct", id: str, props) -> None:
        super().__init__(scope, id)
        StepFunction.__eb_stepfunction = self.create_state_machine(props)

    def create_state_machine(self, props):
        start_state = sfn.Pass(self, "StartState")
        sfn.StateMachine(
            self, 
            id="EBStateMachine",
            state_machine_name=props.step_function_name,
            definition=start_state
        )