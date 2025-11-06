import boto3


from ec2 import Ec2ConfigGenerators
def handler(event, context):
    print(event)
    print("we are going to spin up the EC2 instances")
    print(context)

    ec2_client = boto3.client("ec2", region_name=event["region"])
    ssm_client = boto3.client("ssm", region_name=event["region"])
    ec2_configuration = Ec2ConfigGenerators(event)
    print(ec2_configuration)
    # aml2023 ami-0157af9aea2eef346
    instance = ec2_client.run_instances(
        ImageId= "ami-0157af9aea2eef346",
        MinCount=1,
        MaxCount=1,
        InstanceType=ec2_configuration.instance_type,
        UserData=ec2_configuration.user_data,
        IamInstanceProfile=ec2_configuration.iam_profile,
        InstanceInitiatedShutdownBehavior="terminate",
        MetadataOptions= {'HttpTokens': 'required'},
        SecurityGroupIds=ec2_configuration.security_group_ids,
        SubnetId=ec2_configuration.subnet_id,
        TagSpecifications=[
            {'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'cogesak-flamethrower-infra'}]}
        ]

    )
    running_instance_id = instance['Instances'][0]['InstanceId']
    print(f"\nInstance ID: {running_instance_id}")

    ### Code to Connect via SSM didnt Work as Expected so we are sticking with the user data

    # VENV_PATH = '/home/ec2-user/flame'
    # PYTHON_SCRIPT = """
    #         import sys
    #         import os
    #         import requests
    #
    #         print("--- VENV CHECK ---")
    #         print(f"Python Executable: {sys.executable}")
    #         print(f"VIRTUAL_ENV variable: {os.environ.get('VIRTUAL_ENV', 'Not Set')}")
    #         print(f"Requests Version: {requests.__version__}")
    #     """
    # COMMAND_STRING = f"""
    #     echo "Starting inline Python execution inside Venv..."
    #
    #     sudo -u ec2-user bash -c 'echo "{PYTHON_SCRIPT}" | {VENV_PATH}/bin/python3'
    #
    # """
    # # Execute a python Command via SSM
    # command_response = ssm_client.send_command(
    #     InstanceIds=[running_instance_id],
    #     DocumentName='AWS-RunShellScript',
    #     Parameters={'commands': [COMMAND_STRING]},
    #     Comment='Executing Python script inside existing virtual environment',
    #     TimeoutSeconds=600,
    # )
    # command_id = command_response['Command']['CommandId']
    # print(f"Command sent successfully. Command ID: {command_id}")





    return {
        "ec2" : str(instance)
    }



