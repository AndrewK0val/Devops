import boto3

BUCKET_NAME=''
AWS_REGION=''


def create_s3_bucket_using_client(bucket_name, aws_region):
    s3_client = boto3.client('s3')
    s3_bucket_location = {'LocationConstraint': aws_region}

    response  = s3_client.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration=s3_bucket_location
    )

    return response

if __name__ == '__main__':
    create_s3_bucket_using_client(BUCKET_NAME, AWS_REGION)
    print(f"AWS s3 bucket '{BUCKET_NAME}' has been created")