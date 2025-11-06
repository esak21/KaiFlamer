#!/bin/sh

log_print() {
  echo "::::::::::::::::::::::::::::::::::::::::::::"
  echo "${i}"
  echo "::::::::::::::::::::::::::::::::::::::::::::"
}
echo "Lets install the User data Script "
REGION="<<cloudwatch-region>>"
ENV="<<deploy_env>>"
LOG_GROUP_NAME="/aws/ec2/cogesak-flamer-ec2-${ENV}-logs"
LOG_STREAM_DATE=$(date +"%Y/%m/%d")
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
echo $INSTANCE_ID
log_print "STARTING THE CLOUDWATCH AGENT"
### Creating the Cloud watch Log Group

sudo aws logs create-log-group --log-group-name $LOG_GROUP_NAME --region $REGION

### Installing the Cloud watch Agent
echo "Downloading the CloudWatch Agent"
wget https://s3.amazonaws.com/amazoncloudwatch-agent/amazon_linux/amd64/latest/amazon-cloudwatch-agent.rpm

sudo rpm -U ./amazon-cloudwatch-agent.rpm
echo "Agent Installed"


echo "Creating the Cloudwatch agent configuration File"
sudo bash -c """cat  <<EOT > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  \"agent\" : {
      \"run_as_user\" : \"root\"
    },
    \"logs\" : {

          \"force_flush_interval\" : 5,
          \"logs_collected\" : {
              \"files\" : {
                      \"collect_list\" : [
                          {
                            \"file_path\" : \"/home/ec2-user/snowmobile.log\",
                            \"log_group_name\" : \"${LOG_GROUP_NAME}\",
                            \"log_stream_name\" : \"${LOG_STREAM_DATE}/${INSTANCE_ID}\"
                          }
                      ]
              }
            }
        }
}
EOT
"""

echo "Starting the Cloudwatch Agent"

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a start

echo "Agent Started"

# Lets Add EBS Volumes


aws s3 cp s3://cogesak-etl-target/reports/ec2_runner.py .
chmod 777 $HOME/ec2_runner.py


# install the Python3.11
sudo dnf update -y
sudo dnf install python3.11 -y

sudo dnf install python3.11-pip -y
python3.11 --version

# Navigate to your user's home directory
cd /home/ec2-user

# Create the venv using Python 3.11
python3.11 -m venv my_app_venv

# Activate the virtual environment
source my_app_venv/bin/activate

# This uses the 'pip' inside the active venv
pip install requests  pandas  boto3

# Run the script using the Python interpreter inside the active venv
python $HOME/ec2_runner.py


echo "Script executed Successfully"



