import boto3


from ec2 import Ec2ConfigGenerators
def handler(event, context):
    print(event)
    print("we are going to spin up the EC2 instances")
    print(context)

    ec2_client = boto3.client("ec2", region_name=event["region"])

    ec2_configuration = Ec2ConfigGenerators(event)
    print(ec2_configuration)

    instance = ec2_client.run_instances(
        ImageId= ec2_configuration.ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=ec2_configuration.instance_type,
        UserData=ec2_configuration.user_data,
        IamInstanceProfile=ec2_configuration.iam_profile,
        InstanceInitiatedShutdownBehavior="terminate",
        MetadataOptions= {'HttpTokens': 'required'},

    )

    return {
        "ec2" : str(instance)
    }



