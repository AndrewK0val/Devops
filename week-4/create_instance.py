import boto3
import webbrowser
import sys
import time
import datetime


private_key_path = 'your-private-key.pem'

s3 = boto3.resource("s3")

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


# s3 bucket code
#---------------------------------------------------------
bucket_name = "projectx-bucket1-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
    response = s3.create_bucket(Bucket=bucket_name)
    print(response)
except Exception as error:
    print(error)



website_configuration = { 
    'ErrorDocument': {'Key': 'error.html'}, 
    'IndexDocument': {'Suffix': 'index.html'}, 
} 
 
bucket_website = s3.BucketWebsite({bucket_name})   # replace with your  bucket name or a string variable
 
 
response = bucket_website.put(WebsiteConfiguration=website_configuration)


print("Opening the web browser...")
time.sleep(60)
# I know that giving it a delay is not ideal but I wasnt able to figure out
# a better solution in time
webbrowser.open_new_tab(f'http://{public_ip}')

# There was this bug which was driving me mad for 2 hours.
# I was doing webbrowser.open_new_tab(f"http://{public_ip}")
# and my browser for some reason was defaulting to https and not http
# I never thought that using a different type of quotation symbol 
# made a difference in the protocol the web browser will try to use but
# now I know this is important

# Generate a unique bucket name using the current date and time
