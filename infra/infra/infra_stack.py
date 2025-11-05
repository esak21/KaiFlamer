from constructs import Construct

from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    Duration
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

