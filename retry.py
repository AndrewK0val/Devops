import boto3
import botocore
import time

# Create an EC2 client
ec2 = boto3.client('ec2')

# Define the parameters for launching the EC2 instance
instance_params = {
    'ImageId': 'ami-00c6177f250e07ec1',  # Specify the desired AMI ID
    'MinCount': 1,
    'MaxCount': 1,
    'InstanceType': 't2.nano',          # Specify the instance type
    'KeyName': 'DevopsAWSKeys',    # Specify your key pair name
}

# Launch the EC2 instance
response = ec2.run_instances(**instance_params)

# Extract the instance ID
instance_id = response['Instances'][0]['InstanceId']

print(f"Launched EC2 instance with ID: {instance_id}")

# Retry with exponential backoff
max_retries = 5
retry_delay = 2  # Initial retry delay in seconds

for i in range(max_retries):
    try:
        # Describe the instance to get its public IP address
        response = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        break  # If successful, exit the loop
    except botocore.exceptions.ClientError as e:
        if 'RequestExpired' in str(e):
            # If it's a RequestExpired error, retry after a delay
            print(f"Retry {i+1} - RequestExpired error, retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
            retry_delay *= 2  # Exponential backoff
        else:
            # Handle other errors or raise the exception
            raise

print(f"Public IP address of the instance: {public_ip}")
