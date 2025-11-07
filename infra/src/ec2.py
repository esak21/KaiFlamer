import sys
from pathlib import Path
from ami import get_latest_ami

class Ec2ConfigGenerators:

    def __init__(self, event):
        self.event = event

        if event['region'] == 'us-east-1':
            self.region = 'us-east-1'
        else:
            raise  ValueError("Region must be 'us-east-1' or 'us-east-2'")

        self.environment = self.getEnv()
        self.user_data_file = f"bootsrap.sh"
        self.user_data = self.read_user_data()
        self.ami_id = get_latest_ami('amazon', 'al2023-ami-*x86_64')
        self.instance_type = "t2.micro"
        self.iam_profile = self.assign_iam_profile()
        self.security_group_ids =self.get_security_group_ids()
        self.subnet_id = self.get_subnet_id()


    def assign_iam_profile(self):
        return {"Name": "SimpleDummyRole"}

    def getEnv(self):
        """ Get the environment variables """
        return "qa"

    def get_security_group_ids(self):
        """ Get the security group ids """
        return ["sg-05e5b31eaeb21d0c0"]

    def get_subnet_id(self):
        """ Get the subnet id """
        return "subnet-04796085a84126541"

    def read_user_data(self):
        """ Read the user data from the Bootstrap Scripts """
        print(sys.path[1])
        with open(self.user_data_file, "r") as file:
            user_data = file.read()

        user_data = user_data.replace("<<cloudwatch-region>>", "us-east-1")
        user_data = user_data.replace("<<deploy_env>>", self.getEnv())



        print(user_data)
        return user_data




if __name__ == "__main__":
    user_event = {
        "region": "us-east-1",
    }
    ec2_configuration = Ec2ConfigGenerators(user_event)
    print(ec2_configuration.ami_id)


