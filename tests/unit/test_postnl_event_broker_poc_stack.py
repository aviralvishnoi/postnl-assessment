import aws_cdk as core
import aws_cdk.assertions as assertions

from postnl_event_broker_poc.postnl_event_broker_poc_stack import (
    PostnlEventBrokerPocStack,
)

# example tests. To run these tests, uncomment this file along with the example
# resource in postnl_event_broker_poc/postnl_event_broker_poc_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PostnlEventBrokerPocStack(app, "postnl-event-broker-poc")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
