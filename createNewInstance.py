import boto3

ec2 = boto3.resource('ec2')

instance_list = []
for inst in ec2.instances.all():
    instance_list.append(inst)

print (instance_list[0].image_id)
instance_list[0].stop()



