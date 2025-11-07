from constructs import Construct

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    Duration,
    aws_s3 as _s3,
    aws_s3_deployment as s3_deployment,
                      )

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Let's Create the lambda
        flamer_infra_builder  = _lambda.Function( self,
            "FlamerInfraBuilder",
            function_name="FlamerInfraBuilder",
            runtime=_lambda.Runtime.PYTHON_3_11,
            code = _lambda.Code.from_asset("src"),
            handler= "handler.handler",
        )

        # copy a Script to S3 Bucket
        bucket_name = _s3.Bucket.from_bucket_name(
            self, "ExistingBucket", "cogesak-etl-target"
        )

        s3_deployment.BucketDeployment(
            self,
            "S3Deployment",
            sources= [s3_deployment.Source.asset("infra/resources/")], # Specify the local file path
            destination_bucket= bucket_name,
            destination_key_prefix="reports" # Optional: Specify a different key for the uploaded file
        )


