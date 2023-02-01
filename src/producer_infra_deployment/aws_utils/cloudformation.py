import boto3
from botocore.exceptions import ClientError

cft_client = boto3.client("cloudformation")

class CFT:

    def __init__(self, stack_name, stack_parameters) -> None:
        self.stack_name = stack_name
        self.stack_parameters = stack_parameters

    def get_stack_status(self):
        try:
            response = cft_client.describe_stacks(StackName = self.stack_name)
            stack_status = response.get("Stack")[0]["StackStatus"]
        except ClientError:
            return False
        return stack_status

    def create_stack(self):
        try:
            response = cft_client.create_stack(
                StackName=self.stack_name,
                #TODO: Read template from s3 bucket
                TemplateURL="s3://",
                Parameters = self.stack_parameters,
                Capabilities = "CAPABILITY_NAMED_IAM"
            )
        except ClientError as e:
            return str(e)
        return response

    def update_stack(self):
        try:
            response = cft_client.update_stack(
                StackName=self.stack_name,
                #TODO: Read template from s3 bucket
                TemplateURL="s3://",
                Parameters = self.stack_parameters,
                Capabilities = "CAPABILITY_NAMED_IAM"
            )
        except ClientError as e:
            return str(e)
        return response
    
    def check_stack_exists(self):
        try:
            cft_client.describe_stacks(StackName = self.stack_name)
        except ClientError:
            return False
        return True

    def stack_requester(self):
        stack_exists = self.check_stack_exists()
        if stack_exists:
            stack_status = self.get_stack_status()
            if stack_status in ("CREATE_COMPLETE", "UPDATE_COMPLETE"):
                self.update_stack()
            elif stack_status == "CREATE_IN_PROGRESS":
                print("Stack Creation in progress")
            else:
                print("For now I am not handling other stack status")
        else:
            create_stack_response = self.create_stack()
            if isinstance(create_stack_response, dict):
                print("Stack creation initiated")
            else:
                print(f"There was an error during creation of stack {create_stack_response}")
        
        
        