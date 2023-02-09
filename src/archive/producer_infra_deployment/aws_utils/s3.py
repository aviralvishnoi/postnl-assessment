import boto3

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")

class S3:
    
    def __init__(self, s3_bucket_name) -> None:
        self.s3_bucket_name = s3_bucket_name

    def get_object_from_s3(self, object_key):
        pass
