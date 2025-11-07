# KaiFlamer
Load the data from postgres to iceDancer
Lets Create CDK project 

Prerequisites for Command Execution
To successfully execute a command remotely after launch, the new EC2 instance must meet these criteria:

IAM Role: The instance must have an IAM Instance Profile attached that includes the AmazonSSMManagedInstanceCore policy.

AMI: The Amazon Machine Image (ImageId) must have the SSM Agent pre-installed (e.g., all current Amazon Linux, Ubuntu, and Windows AMIs).

Networking: The instance needs outbound connectivity (HTTPS port 443) to the SSM service endpoint.

Enforcing IMDSv2: Cloud providers (like AWS) recommend enforcing IMDSv2 via the MetadataOptions setting on the instance. IMDSv2 requires a secret, token-based session before any metadata can be accessed, which usually defeats simple SSRF exploits.

## Set up the Security Groups 
we need to open the Port 443 if we want to use the SSM and its send commands

## Setting up the IAM Role
we need to Provide the below Policy in EC2 Roles 
1. AmazonEC2FullAccess
2. AmazonS3FullAccess
3. CloudWatchAgentServerPolicy
4. AmazonSSMManagedInstanceCore
5. To Create the Subscription filter we need to add the Below Role 
   ```{
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "logs:PutSubscriptionFilter",
               "Resource": "arn:aws:logs:us-east-1:905418448077:log-group:/aws/ec2/cogesak-flamer-ec2-qa-logs:*"
           },
           {
               "Effect": "Allow",
               "Action": "iam:PassRole",
               "Resource": "arn:aws:iam::905418448077:role/simpleFirehouseRole"
           }
       ]
   }
   ```

we need to Provide the below Policy in LAMBDA Roles 
1. AWSLambdaBasicExecutionRole
2. AmazonEC2FullAccess -> to Create the EC2 instance 
3. we need to provide the IAM pass role to the lambda IAM so that the Ec2 instance will be created
   ````
           {
               "Effect": "Allow",
               "Action": "iam:PassRole",
               "Resource": "arn:aws:iam::<ACCOUNT_ID>:role/SimpleDummyRole"
           }
           ````
4. 

## Create Kinesis Firehouse IAM Role 
1. AmazonKinesisFirehoseFullAccess
```commandline

```
we can provide the s3 prefix as below 
`raw_logs/!{timestamp:yyyy}-!{timestamp:MM}-!{timestamp:dd}/`

Command to Verify the user data executed correct or not 
```
# After logging into the instance (via Session Manager or SSH)
tail -100 /var/log/cloud-init-output.log

# View the actual script file that was executed
sudo cat /var/lib/cloud/instance/scripts/part-001
```
## step 3: Manually Execute the Script
If the logs are still unclear, you can re-run the script manually on the live instance to reproduce the error in an interactive environment.


```
# View the contents of the script cloud-init attempted to run
sudo cat /var/lib/cloud/instance/scripts/part-001

# Run the script with the verbose flag to debug execution line-by-line
sudo /bin/bash -x /var/lib/cloud/instance/scripts/part-001
Running the script with bash -x will show you exactly which line 
of the script fails and what error message the system generates. 
This is the most reliable way to find the root cause.
```

### Lets Create the Kinesis data firehouse to transfer the Logs 
