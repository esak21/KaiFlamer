import requests

print(f"Requests Version: {requests.__version__}")
import logging
import time

# --- Configuration ---
# Set up the root logger to write to a file. This only runs once.
logging.basicConfig(
    # 1. Filename: The log file will be created if it doesn't exist.
    filename='snowmobile.log',

    # 2. Level: Only log messages at this level or higher (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    level=logging.INFO,

    # 3. Format: Defines the structure of each log entry
    format='%(asctime)s - %(levelname)s - %(message)s',

    # 4. File Mode: 'a' (append) adds new logs; 'w' (write) overwrites the file each run.
    filemode='a'
)

import boto3

# --- Configuration ---
# You MUST change this to the region where the AMI ID ami-0ba15e2c4dcffba60 is located
REGION = 'us-east-1'
AMI_ID = 'ami-0ba15e2c4dcffba60'

# Create the EC2 client
ec2_client = boto3.client('ec2', region_name=REGION)

try:
    response = ec2_client.describe_images(
        ImageIds=[AMI_ID]
    )

    if response['Images']:
        image_details = response['Images'][0]

        logging.info(f"--- Details for AMI ID: {AMI_ID} in {REGION} ---")
        logging.info(f"Name: {image_details.get('Name', 'N/A')}")
        logging.info(f"Description: {image_details.get('Description', 'N/A')}")
        logging.info(f"Platform: {image_details.get('Platform', 'Linux (Default)')}")
        logging.info(f"Platform Details: {image_details.get('PlatformDetails', 'N/A')}")
        logging.info(f"Owner ID: {image_details.get('OwnerId')}")
    else:
        logging.info(f"❌ AMI ID {AMI_ID} not found or you lack permissions to view it in {REGION}.")

except Exception as e:
    logging.error(f"An error occurred: {e}")


# --- Writing Log Messages ---
logging.debug('This is a detailed debug message for developers.')
logging.info('Application started successfully.')

time.sleep(1)  # Wait a second to show the timestamp changes
logging.warning('The operation finished, but a minor issue was noted.')