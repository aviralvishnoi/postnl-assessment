from aws_cdk import aws_apigateway as _apigateway, aws_lambda as _lambda
from constructs import Construct
from dataclasses import dataclass


@dataclass
class ApiGatewayProps:
    deploy_environment: str
    rest_api_name: str
    usage_plan_name: str
    producer_lambda: _lambda.Function


class ApiGateway(Construct):
    def __init__(
        self, scope: "Construct", construct_id: str, props: ApiGatewayProps
    ) -> None:
        super().__init__(scope, construct_id)
        ApiGateway.__eb_apigateway = self.create_rest_api(props)

    def create_rest_api(self, props):
        # Create stage options
        eb_deploy_stage = _apigateway.StageOptions(
            stage_name=f"{props.deploy_environment}"
        )
        # Create REST Api
        eb_apigateway = _apigateway.RestApi(
            self, "EBApiGateway", rest_api_name=f"{props.rest_api_name}", deploy_options=eb_deploy_stage
        )
        # Add lambda integration
        eb_integration = _apigateway.LambdaIntegration(
            props.producer_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        # Add method
        eb_apigateway.root.add_method("GET", eb_integration)

        # Create usage plan
        eb_plan = eb_apigateway.add_usage_plan(
            "EBUsagePlan",
            name=f"{props.usage_plan_name}",
            throttle=_apigateway.ThrottleSettings(rate_limit=10, burst_limit=2),
        )
        # Create api key
        eb_key = eb_apigateway.add_api_key("ApiKey")
        # Add api key
        eb_plan.add_api_key(eb_key)

        # Create deployment
        eb_deployment = _apigateway.Deployment(
            self, "EBDeployment",
            api=eb_apigateway
        )

        # Stage creation
        # _apigateway.Stage(
        #     "EBStage",
        #     deployment=eb_deployment
        # )

