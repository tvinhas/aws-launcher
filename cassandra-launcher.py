#!/usr/bin/env python
########################################################################################################
#                                                                                                      #
#  Cassandra cluster launcher                                                                          #
#  Developed by Thiago Vinhas <thiago@vinhas.org>                                                      #
#                                                                                                      #
########################################################################################################

import boto3
import json
import argparse

##############################################
####           AWS Credentials            ####
##############################################

conn = {
    'aws_access_key_id': '---ADD-YOUR-KEY-ID---',
    'aws_secret_access_key': '---ADD-ACCESS-KEY---',
    'region_name': 'us-east-1'
}

userdata = "#!/bin/bash \n aws s3 cp s3://tvinhas-scripts/cassandra-userdata.sh .\n bash cassandra-userdata.sh" 
key = 'tvinhas-ncloud'
securitygroup = 'sg-7d256706'
instanceprofile = 'arn:aws:iam::686787828286:instance-profile/ncloud'

parser = argparse.ArgumentParser(description='You are fine with the defaults...')
parser.add_argument('-a', '--ami', action="store", dest="ami", default="ami-6869aa05", help="Define the AMI to be used")
parser.add_argument('-s', '--subnet', action="store", dest="subnet", default="subnet-23dc877b", help="Define the subnet to be used")
parser.add_argument('-i', '--instancetype', action="store", dest="instancetype", default="t2.large", help="Define the instance type")

args = parser.parse_args()
ami = args.ami
subnet = args.subnet
instancetype = args.instancetype

##############################################
####           Launch Instance 1          ####
##############################################

print "Launching Instance cassandra1..."

ec2 = boto3.resource('ec2', **conn)
create_instance = ec2.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    KeyName=key,
    InstanceType=instancetype,
    SecurityGroupIds=[securitygroup],
    UserData=userdata,
    IamInstanceProfile={
        'Arn': instanceprofile
    },
    SubnetId=subnet
)

instanceid = create_instance[0].id
instance = create_instance[0]

# Tag instance
client = boto3.client('ec2', **conn)
client.create_tags(
    Resources = [instanceid], 
    Tags= [{"Key": "Name", "Value": "cassandra1"}]
)

instance.wait_until_running()
instance.load()

print "Created new instance with id %s" % instanceid 
print "IP Address: %s" % instance.public_ip_address
print "Instance Type: %s\n" % instancetype


##############################################
####           Launch Instance 2          ####
##############################################

print "Launching Instance cassandra2..."

ec2 = boto3.resource('ec2', **conn)
create_instance = ec2.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    KeyName=key,
    InstanceType=instancetype,
    SecurityGroupIds=[securitygroup],
    UserData=userdata,
    IamInstanceProfile={
        'Arn': instanceprofile
    },
    SubnetId=subnet
)

instanceid = create_instance[0].id
instance = create_instance[0]

# Tag instance
client = boto3.client('ec2', **conn)
client.create_tags(
    Resources = [instanceid], 
    Tags= [{"Key": "Name", "Value": "cassandra2"}]
)

instance.wait_until_running()
instance.load()

print "Created new instance with id %s" % instanceid 
print "IP Address: %s" % instance.public_ip_address
print "Instance Type: %s\n" % instancetype


##############################################
####           Launch Instance 3          ####
##############################################

print "Launching Instance cassandra3..."

ec2 = boto3.resource('ec2', **conn)
create_instance = ec2.create_instances(
    ImageId=ami,
    MinCount=1,
    MaxCount=1,
    KeyName=key,
    InstanceType=instancetype,
    SecurityGroupIds=[securitygroup],
    UserData=userdata,
    IamInstanceProfile={
        'Arn': instanceprofile
    },
    SubnetId=subnet
)

instanceid = create_instance[0].id
instance = create_instance[0]

# Tag instance
client = boto3.client('ec2', **conn)
client.create_tags(
    Resources = [instanceid], 
    Tags= [{"Key": "Name", "Value": "cassandra3"}]
)

instance.wait_until_running()
instance.load()

print "Created new instance with id %s" % instanceid 
print "IP Address: %s" % instance.public_ip_address
print "Instance Type: %s\n" % instancetype


