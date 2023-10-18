import boto3
import webbrowser
import sys
import time
import datetime
import random
import string


private_key_path = 'your-private-key.pem'

s3 = boto3.resource("s3")

ec2 = boto3.client('ec2')

user_data_script = """#!/bin/bash
yum install httpd -y
systemctl enable httpd
systemctl start httpd

INSTANCE_TYPE="t2-nano"
AVILABILITY_ZONE="us-east-1"
ADDITIONAL_TEXT="abcdefg"
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

#You should name your bucket using a combination of 6 random characters and your
#name; e.g. 1a2b3c-jbloggs replacing 1a2b3c with random characters and jbloggs with your first
#initial and last name. 
lenght = 6
sixRandomChars = ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))



bucket_name = sixRandomChars + "-akoval"

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



webbrowser.open_new_tab(f'http://{public_ip}')

