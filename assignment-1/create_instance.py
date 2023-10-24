import boto3
import webbrowser
import sys
import time
import datetime
import random
import string
import subprocess
import json
 

OBJECT_NAME = '/home/andrew/Devops/script.js'
AWS_REGION='us-east-1'
OBJECT_1 = 'index.html'
OBJECT_2 = 'logo.jpg'
AWS_REGION='us-east-1'
keyName='CA-1-key'
instances = []

def random_chars(lenght):
    RANDOM_CHARS = ''.join(random.choices(string.ascii_lowercase + string.digits, k=lenght))
    return RANDOM_CHARS

BUCKET_NAME=f'{random_chars(6)}-akoval'


private_key_path = 'your-private-key.pem'
s3_client = boto3.client('s3')
s3_resource = boto3.resource("s3")
ec2_client = boto3.client('ec2', region_name='us-east-1')
ec2 = boto3.resource('ec2', region_name='us-east-1')

user_data_script = """#!/bin/bash
    yum update -y
    yum install httpd -y
    yum install -y mariadb-server
    yum install php -y

    systemctl enable httpd
    systemctl start httpd

    INSTANCE_TYPE="t2-nano"
    AVILABILITY_ZONE="us-east-1"
    ADDITIONAL_TEXT="abcdefg"




    cd /var/www/html
    echo '<html>' > index.html
    echo '<a href="index.html">Home</a> | <a href="monitoring.html">Monitoring Stats</a><br><br>' >> index.html
    echo '<ul>' >> index.html
    echo '<li>Private IP address: ' >> index.html
    curl http://169.254.169.254/latest/meta-data/local-ipv4 >> index.html
    echo " Public IP address" >> index.html
    curl http://169.254.169.254/latest/meta-data/public-ipv4 >> index.html 
    echo '</li>' >> index.html
    echo '<li>Instance AMI: ' >> index.html
    curl -s http://169.254.169.254/latest/meta-data/ami-id >> index.html
    echo '</li>' >> index.html
    echo '<li>Availability Zone: ' >> index.html
    curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone >> index.html
    echo '</li>' >> index.html
    echo '<li>Instance ID: ' >> index.html
    curl -s http://169.254.169.254/latest/meta-data/instance-id >> index.html
    echo '</li>' >> index.html
    echo '<li>Instance Type: ' >> index.html
    curl -s http://169.254.169.254/latest/meta-data/instance-type >> index.html
    echo '</li>' >> index.html
    echo '</ul>' >> index.html
    cp index.html /var/www/html/index.html

"""


def userMenu():
    option = input("Please select an option: \n1. Create instance \n2. Create s3 bucket \n3. View bucket details \n4. CloudWatch \n 5. Exit \n")

    match option:
        case "1":
            create_instance()
        case "2":
            create_s3_bucket(OBJECT_1, OBJECT_2, BUCKET_NAME)
        case "3":
            view_bucket_details()
        case "4":
            cloudWatch()

        case "5":
            exit()



def download_image():
    URL = "http://devops.witdemo.net/logo.jpg"
    response = requests.get(URL)

    file = open("logo.jpg", "wb")
    file.write(response.content)
    file.close()


def create_instance():
    try:
        print('creating instance...')
        instance = ec2.create_instances(
            ImageId='ami-00c6177f250e07ec1',
            InstanceType='t2.nano',
            MinCount=1,
            MaxCount=1,
            KeyName=keyName,
            SecurityGroups=['launch-wizard-1'],
            SecurityGroupIds=['sg-03328d5226bccd389'],
            UserData=user_data_script
        )

        instance_id = instance[0].id
        ec2.create_tags(Resources=[instance_id], Tags=[{'Key': 'Web server', 'Value': 'AssignmentInstance'}]) 
    
        instance[0].wait_until_running() #Wait for the instance to be up and running
        instance[0].reload() #Reload the instance to ensure it reflects the current state
        # Launch the EC2 instance
        # response = ec2.run_instances(**instance_params)

        # Extract the instance ID
        # ipAddr = ec2.instances.all().Private_IP_Address

        print(f"Launched EC2 instance with ID: {instance_id}")
        # Wait for the instance to be in a running state
        ec2_client.get_waiter('instance_running').wait(InstanceIds=[instance_id])
        # Describe the instance to get its public IP address

        subprocess.run("chmod 400 " + str(keyName) + ".pem", shell=True)
        subprocess.run("scp -i " + str(keyName) + ".pem" + " -o StrictHostKeyChecking=no monitoring.sh ec2-user@" +
        str(instance[0].public_ip_address) + ":." , shell=True)
        print("Waiting for instance initialization")
        time.sleep(60)

        print("checking scp connection")
        subprocess.run("ssh -i "+ str(keyName) + ".pem" + " ec2-user@" + str(instance[0].public_ip_address) + " 'chmod 700 monitoring.sh'", shell = True)
        print("checking ssh connection")
        subprocess.run("ssh -i " + str(keyName) + ".pem" + " ec2-user@" + str(instance[0].public_ip_address) + " ' ./monitoring.sh'", shell = True)
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
        print(f"Public IP address of the instance: {public_ip}")

    except Exception as e:
        print(f"An error occurred while creating the EC2 instance: {e}")



# s3 bucket code
#---------------------------------------------------------

# sixRandomChars = ''.join(random.choices(string.ascii_letters + string.digits, k=lenght))




def create_s3_bucket(OBJECT_1, OBJECT_2, BUCKET_NAME):
    
    website_configuration = { 
            'ErrorDocument': {'Key': 'error.html'}, 
            'IndexDocument': {'Suffix': 'index.html'}, 
        } 
    s3_bucket = boto3.resource("s3") 
    if __name__ == '__main__':
        print("making bucket...")
    try:
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
        webbrowser.open_new_tab(f'http://{BUCKET_NAME}.s3-website.{AWS_REGION}.amazonaws.com')
    except Exception as error:
        print(error)

def view_bucket_details():
    try:
        for bucket in s3_resource.buckets.all():
            print(bucket.id, bucket.state, bucket.public_ip_address)
    except Exception as e:
        print(e)

# create_instance()
# create_s3_bucket(OBJECT_1, OBJECT_2, BUCKET_NAME)


# print("Opening the web browser...")
# time.sleep(30)



def cloudWatch():
    try: 
        instance_id = instances[0].id
    except Exception as e:
        print(e)

def exit():
    sys.exit()
        
userMenu()