from operator import itemgetter

import boto3

ec2_client = boto3.client("ec2", region_name="us-east-1")

def get_latest_ami(owner, ami_name_pattern):
    """ Get the latest AMI from the AMI registry."""
    amazon_linux_filters = [
        {'Name': 'name', 'Values': ['amzn2-ami-hvm-*-x86_64-gp2']}
    ]
    response = ec2_client.describe_images(
        Owners=[owner],
        Filters=[
            {'Name': 'name', 'Values': [ami_name_pattern]},
            {'Name': 'state', 'Values': ['available']}
        ]
    )

    latest_image = sorted(response['Images'], key=itemgetter('CreationDate'), reverse=True)[0]

    print(latest_image['ImageId'])
    return latest_image['ImageId']


if __name__ == "__main__":
    REGION = 'us-east-1'
    OWNER_ACCOUNT = 'amazon'
    AMI_PATTERN = 'amzn2-ami-hvm-*-x86_64-gp2'
    get_latest_ami(OWNER_ACCOUNT, AMI_PATTERN)