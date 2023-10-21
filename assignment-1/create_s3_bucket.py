import boto3
import string
import random

lenght = 6
sixRandomChars = ''.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))
OBJECT_NAME = '/home/andrew/Devops/script.js'

BUCKET_NAME=f'{sixRandomChars}-akoval'
AWS_REGION='us-east-1'


def create_s3_bucket_using_client(bucket_name, aws_region):
    s3_client = boto3.client('s3')
    # s3_bucket_location = {'LocationConstraint': aws_region}

    response  = s3_client.create_bucket(
        Bucket=bucket_name
        # CreateBucketConfiguration=s3_bucket_location
    )

    return response


def put_stuff_in_bucket(OBJECT_NAME, BUCKET_NAME):
    s3_bucket = boto3.resource("s3") 


    if __name__ == '__main__':
        create_s3_bucket_using_client(BUCKET_NAME, AWS_REGION)
        print(f"AWS s3 bucket '{BUCKET_NAME}' has been created")

    try:
        response = s3_bucket.Object(BUCKET_NAME, OBJECT_NAME).put(
            Body=open(OBJECT_NAME, 'rb'))
        print(response)
    except Exception as error:
        print(error)