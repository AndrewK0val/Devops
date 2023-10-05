import boto3

# Create an EC2 client
ec2 = boto3.client('ec2')

# Describe all key pairs
response = ec2.describe_key_pairs()

# Extract the key pairs
key_pairs = response['KeyPairs']

# Print the key pair names
for key_pair in key_pairs:
    print(f"Key Pair Name: {key_pair['KeyName']}")
