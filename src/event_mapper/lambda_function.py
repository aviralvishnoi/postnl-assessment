from crhelper import CfnResource
import boto3

helper = CfnResource(json_logging=False, log_level="INFO", boto_level="CRITICAL")


    
event_bridge_client = boto3.client("events")

def generate_rule_name(event):
    return event["ResourceProperties"]["EventRuleName"]

def extract_sqs_arn(event):
    return event["ResourceProperties"]["SQSArn"]

@helper.create
def create(event: dict, _) -> None:
    sqs_arn = extract_sqs_arn(event)
    rule_name = generate_rule_name(event)
    response = event_bridge_client.put_targets(
            Rule=rule_name,
            EventBusName="arn:aws:events:eu-central-1:320722179933:event-bus/default",
            Targets=[
                {
                    "Id":"ConsumerMapper",
                    "Arn": sqs_arn 
                }
            ]
        )
    print(response)

@helper.update
def update(event: dict, _):
    pass

@helper.delete
def delete(event: dict, _):
    pass
    
def lambda_handler(event, context):
    print(event)
    helper(event, context)
