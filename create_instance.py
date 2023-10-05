import boto3

ec2 = boto3.client('ec2')

user_data_script = """#!/bin/bash
yum install httpd -y
systemctl enable httpd
systemctl start httpd
"""


instance_params = {
    'ImageId': 'ami-00c6177f250e07ec1', 
    'MinCount': 1,
    'MaxCount': 1,
    'InstanceType': 't2.nano',      
    'KeyName': 'DevopsAWSKeys', 
    'UserData': user_data_script,
    'SecurityGroups': ['launch-wizard-1'] 
}
# Launch the EC2 instance
response = ec2.run_instances(**instance_params)

# Extract the instance ID
instance_id = response['Instances'][0]['InstanceId']

# ipAddr = ec2.instances.all().Private_IP_Address

print(f"Launched EC2 instance with ID: {instance_id}")
# print(ipAddr)

# Wait for the instance to be in a running state
ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

# Describe the instance to get its public IP address
response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print(f"Public IP address of the instance: {public_ip}")


# SSH into the EC2 instance

# Replace 'your-private-key.pem' with the path to your private key file
private_key_path = 'your-private-key.pem'

