import boto3

cft_client = boto3.client("cloudformation")

class CFT:

    def __init__(self, stack_name, stack_parameters) -> None:
        self.stack_name = stack_name
        self.stack_parameters = stack_parameters

    def get_stack_status(self):
        pass

    def create_stack(self):
        pass

    def update_stack(self):
        pass
    
    def check_stack_exists(self):
        pass
    
    def stack_requester(self):
        pass
        
        
        