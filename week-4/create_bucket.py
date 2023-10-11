import boto3
import datetime

s3 = boto3.resource("s3")

# Generate a unique bucket name using the current date and time
bucket_name = "projectx-bucket1-" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
    response = s3.create_bucket(Bucket=bucket_name)
    print(response)
except Exception as error:
    print(error)