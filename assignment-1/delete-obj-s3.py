import boto3

s3 = boto3.resource('s3')
bucket_name = 'projectx-bucket1-2023-10-11-16-37-49'

objects_to_delete = s3.meta.client.list_objects(Bucket=bucket_name)

if 'Contents' in objects_to_delete:
    delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete['Contents']]
    s3.meta.client.delete_objects(Bucket=bucket_name, Delete={'Objects': delete_keys})

    print(f"All objects in {bucket_name} have been deleted.")
else:
    print(f"{bucket_name} is already empty.")