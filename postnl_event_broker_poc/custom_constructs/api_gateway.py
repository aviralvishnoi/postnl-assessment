from aws_cdk import aws_apigateway as _apigateway, aws_lambda as _lambda
from constructs import Construct
from dataclasses import dataclass


@dataclass
class ApiGatewayProps:
    rest_api_name: str
    producer_lambda: _lambda.Function


class ApiGateway(Construct):
    def __init__(
        self, scope: "Construct", construct_id: str, props: ApiGatewayProps
    ) -> None:
        super().__init__(scope, construct_id)
        ApiGateway.__eb_apigateway = self.create_rest_api(props)

    def create_rest_api(self, props):
        eb_apigateway = _apigateway.RestApi(
            self, "EBApiGateway", rest_api_name=f"{props.rest_api_name}"
        )

        eb_integration = _apigateway.LambdaIntegration(
            props.producer_lambda,
            request_templates={"application/json": '{ "statusCode": "200" }'},
        )

        eb_apigateway.root.add_method("GET", eb_integration)
