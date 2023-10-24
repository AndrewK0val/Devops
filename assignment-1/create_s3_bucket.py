import boto3
import string
import random
import json
import webbrowser

s3_resource = boto3.resource("s3")
s3_client = boto3.client('s3')


def random_chars(lenght):
    RANDOM_CHARS = ''.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))
    return RANDOM_CHARS

OBJECT_1 = 'index.html'
OBJECT_2 = 'logo.jpg'

BUCKET_NAME=f'{random_chars(6)}-akoval'
AWS_REGION='us-east-1'

# def create_s3_bucket_using_client(bucket_name, aws_region):
#     # s3_bucket_location = {'LocationConstraint': aws_region}
#     response  = s3_resource.create_bucket(Bucket=bucket_name)
#     s3_client.delete_public_access_block(Bucket=bucket_name)

#     bucket_policy = {
#         "Version": "2012-10-17",
#         "Statement": [
#             {
#                 "Sid": "PublicReadGetObject",
#                 "Effect": "Allow",
#                 "Principal": "*",
#                 "Action": ["s3:GetObject"],
#                 "Resource": f"arn:aws:s3:::{bucket_name}/*"
#             }]
#     }

#     s3_resource.Bucket(bucket_name).Policy().put(Policy=json.dumps(bucket_policy))
#     return response

def create_s3_bucket(OBJECT_1, OBJECT_2, BUCKET_NAME):
    
    website_configuration = { 
            'ErrorDocument': {'Key': 'error.html'}, 
            'IndexDocument': {'Suffix': 'index.html'}, 
        } 
    s3_bucket = boto3.resource("s3") 
    if __name__ == '__main__':
        print("making bucket...")
    try:
        # create_s3_bucket_using_client(BUCKET_NAME, AWS_REGION)

        s3_resource.create_bucket(Bucket=BUCKET_NAME)
        print(f"AWS s3 bucket '{BUCKET_NAME}' has been created")
        s3_client.delete_public_access_block(Bucket=BUCKET_NAME)
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
                }
                ]
            }
        s3_resource.Bucket(BUCKET_NAME).Policy().put(Policy=json.dumps(bucket_policy))
        bucket_website = s3_resource.BucketWebsite(BUCKET_NAME)
        response = bucket_website.put(WebsiteConfiguration=website_configuration)
        response = s3_bucket.Object(BUCKET_NAME, OBJECT_1).put(Body=open(OBJECT_1, 'rb'), ContentType = 'text/html')
        response = s3_bucket.Object(BUCKET_NAME, OBJECT_2).put(Body=open(OBJECT_2, 'rb'), ContentType = 'image/jpeg')

        print(f"AWS s3 bucket '{BUCKET_NAME}' has been created")
        print(f"bucket website:http://{BUCKET_NAME}.s3-website.{AWS_REGION}.amazonaws.com")
        print(response)
    except Exception as error:
        print(error)

create_s3_bucket(OBJECT_1, OBJECT_2, BUCKET_NAME)
webbrowser.open_new_tab(f'http://{BUCKET_NAME}.s3-website.{AWS_REGION}.amazonaws.com')


