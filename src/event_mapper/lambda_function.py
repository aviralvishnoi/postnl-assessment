import boto3

event_bridge_client = boto3.client("events")

def generate_rule_name(event):
    return event["ResourceProperties"]["EventRuleName"]

def extract_sqs_arn(event):
    return event["ResourceProperties"]["SQSArn"]

def lambda_handler(event, context):
    sqs_arn = extract_sqs_arn(event)
    rule_name = generate_rule_name(event)
    if event["RequestType"] != "Delete":
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
        response_data = {'Status': 'SUCCESS', 'Data': {'Message': 'Target Registered'}}
    else:
        #TODO: Remove targets
        response = event_bridge_client.remove_targets(
            Rule=rule_name,
            EventBusName="arn:aws:events:eu-central-1:320722179933:event-bus/default",
            Ids=[sqs_arn]
        )
        response_data = {'Status': 'SUCCESS', 'Data': {'Message': 'Nothing Required'}}
        # Send response back to CloudFormation
    response = boto3.client('cloudformation').send_response(
        StackName=event['StackId'],
        LogicalResourceId=event['LogicalResourceId'],
        PhysicalResourceId='unique_id',
        Status=response_data['Status'],
        Reason='Status updated',
        Data=response_data['Data']
    )

    return response

