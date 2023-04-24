import boto3

# Read instance names from file
with open('instance_names.txt', 'r') as f:
    instance_names = f.read().splitlines()

# Create EC2 client
ec2 = boto3.client('ec2', region_name='us-west-1')

# Retrieve instance information
instance_info = []
for instance_name in instance_names:
    response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_info.append({
                'Instance ID': instance['InstanceId'],
                'IP Address': instance['PrivateIpAddress'],
                'VPC ID': instance['VpcId'],
                'Subnet ID': instance['SubnetId']
            })

# Format instance information as table
table = ''
for info in instance_info:
    table += f"{info['Instance ID']}\t{info['IP Address']}\t{info['VPC ID']}\t{info['Subnet ID']}\n"

# Save table to file
with open('ec2_instance_information.txt', 'w') as f:
    f.write(table)

