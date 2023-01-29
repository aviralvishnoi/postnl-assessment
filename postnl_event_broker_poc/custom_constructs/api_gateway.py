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

    def create_model(self, eb_apigateway, props):
        eb_model = _apigateway.Model(
            self,
            id="EBModel",
            rest_api=eb_apigateway,
            content_type="application/json",
            model_name=f"EBProducerModel{props.deploy_environment.title()}",
            schema=_apigateway.JsonSchema(
                schema=_apigateway.JsonSchemaVersion.DRAFT4,
                title="Producer",
                type=_apigateway.JsonSchemaType.OBJECT,
                required=["producer_name", "source"],
                properties={
                    "producer_name": _apigateway.JsonSchema(
                        type=_apigateway.JsonSchemaType.STRING
                    ),
                    "description": _apigateway.JsonSchema(
                        type=_apigateway.JsonSchemaType.STRING
                    ),
                    "source": _apigateway.JsonSchema(
                        type=_apigateway.JsonSchemaType.STRING
                    ),
                },
            ),
        )
        return eb_model

    def create_rest_api(self, props):
        # Create stage options
        eb_deploy_stage = _apigateway.StageOptions(
            stage_name=f"{props.deploy_environment}"
        )
        # Create REST Api
        eb_apigateway = _apigateway.RestApi(
            self,
            id="EBApiGateway",
            rest_api_name=f"{props.rest_api_name}",
            deploy_options=eb_deploy_stage,
        )
        # Add lambda integration
        eb_integration = _apigateway.LambdaIntegration(
            props.producer_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        # Create Request Validator
        eb_request_validator = _apigateway.RequestValidator(
            self,
            id="EBValidator",
            rest_api=eb_apigateway,
            request_validator_name=f"EBValidator-{props.deploy_environment}",
            validate_request_body=True,
            validate_request_parameters=True
        )

        # Create a resource and post method for the api
        eb_producer = eb_apigateway.root.add_resource("producer")
        eb_method = eb_producer.add_method(
            "POST",
            eb_integration,
            api_key_required=True,
            request_models={
                "application/json": self.create_model(eb_apigateway, props)
            },
            request_validator=eb_request_validator,
        )

        # Create deployment
        _apigateway.Deployment(self, "EBDeployment", api=eb_apigateway)

        # Create usage plan
        eb_plan = eb_apigateway.add_usage_plan(
            id="EBUsagePlan",
            name=f"{props.usage_plan_name}",
            throttle=_apigateway.ThrottleSettings(rate_limit=10, burst_limit=2),
        )
        # Create api key
        eb_key = eb_apigateway.add_api_key("ApiKey")
        # Add api key
        eb_plan.add_api_key(eb_key)

        eb_plan.add_api_stage(
            stage=eb_apigateway.deployment_stage,
            throttle=[
                _apigateway.ThrottlingPerMethod(
                    method=eb_method,
                    throttle=_apigateway.ThrottleSettings(rate_limit=10, burst_limit=2),
                )
            ],
        )
