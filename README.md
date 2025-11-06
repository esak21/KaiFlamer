# KaiFlamer
Load the data from postgres to iceDancer
Lets Create CDK project 

# we need to provide the IAM pass role to the lambda IAM so that the Ec2 instance will be created 
````
{
    "Effect": "Allow",
    "Action": "iam:PassRole",
    "Resource": "arn:aws:iam::<ACCOUNT_ID>:role/SimpleDummyRole"
}
````

Command to Verify the user data executed cirrect or not 
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
Running the script with bash -x will show you exactly which line of the script fails and what error message the system generates. This is the most reliable way to find the root cause.
```


