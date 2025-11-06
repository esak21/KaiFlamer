#!/bin/sh

log_print() {
  echo "::::::::::::::::::::::::::::::::::::::::::::"
  echo "${i}"
  echo "::::::::::::::::::::::::::::::::::::::::::::"
}
echo "Lets install the User data Script "
REGION="<<cloudwatch-region>>"
ENV="<<deploy_env>>"
LOG_GROUP_NAME="/aws/ec2/FLAMER-ec2-${ENV}>"
LOG_STREAM_DATE=$(date +"%Y/%m/%d")
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
echo $INSTANCE_ID
log_print "STARTING THE CLOUDWATCH AGENT"

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
                            \"file_path\" : \"/root/src/snowmobile.log\",
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
