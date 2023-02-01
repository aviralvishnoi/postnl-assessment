from aws_cdk import (
    aws_s3 as s3,
    RemovalPolicy
)

from constructs import Construct
from dataclasses import dataclass

@dataclass
class S3BucketProps:
    bucket_name: str

class S3Bucket(Construct):
    __bucket_name = s3.Bucket

    def __init__(self, scope: Construct, construct_id: str, props: S3BucketProps) -> None:
        super().__init__(scope, construct_id)
        S3Bucket.__bucket_name = self.create_s3_bucket(props)

    @property
    def get_bucket_name(self):
        return S3Bucket.__bucket_name.bucket_name

    @property
    def get_bucket_arn(self):
        return S3Bucket.__bucket_name.bucket_arn
        
        
    def create_s3_bucket(self, props):
        s3_bucket = s3.Bucket(
            self,
            "ArtifactS3Bucket",
            bucket_name=props.bucket_name,
            versioned=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            removal_policy=RemovalPolicy.DESTROY
        )
        return s3_bucket