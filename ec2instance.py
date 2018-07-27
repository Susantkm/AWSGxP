#!/usr/bin/env python

import sys
import json
import csv
import re
import maths
import boto3
from botocore.exceptions import ClientError
import pandas as pd
import numpy as np

cfn = boto3.client('cloudformation')
S3 = boto3.client('s3')
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
iam = boto3.client('iam')
#role = iam.Role()


# To get cloudformation status with input, output, tags etc

rspnse =  cfn.describe_stacks(StackName='diabetes-immersionday-stack')   
df = pd.DataFrame(rspnse['Stacks'])
df.to_csv('cfn-desc-resources-iq.csv')

# To get ALl Resource Stacks and their details
rspnse =  cfn.describe_stack_resources(StackName='diabetes-immersionday-stack')   
df1 = pd.DataFrame(rspnse['StackResources'])
df1.to_csv('resource-stacks-iq.csv')
print("success")

#read the csv file to get resource type and Physical resource ID
csv_file = 'resource-stacks-iq.csv'
csvReader = pd.read_csv(csv_file)
fieldnames = ['PhysicalResourceId','ResourceType']
csvReader1 = csvReader[fieldnames]
# loop to get each record for resource type and Physical resource ID and then get instance description

for i in  csvReader.index:
    restype = csvReader['ResourceType'][i]
    physicalresId = csvReader['PhysicalResourceId'][i]
    
    if "AWS::RDS::DBInstance" in restype:
       print ('rds is dd1mq3dczxgr5jn', physicalresId)
       rdsresponse = rds.describe_db_instances(DBInstanceIdentifier=physicalresId)
       dfrds = pd.DataFrame(rdsresponse['DBInstances'])
       dfrds.to_csv('rds-dbinstancedesc-iq.csv')
       #print('successful-rds')
    elif  "AWS::EC2::Instance" in restype:
        print ('Ec2')
        #print (resourceId)
        ec2response = ec2.describe_instances(InstanceIds=[physicalresId])
        #print (ec2response) 
        dfec2 = pd.DataFrame(ec2response['Reservations'])
        dfec2.to_csv('ec2-instancedesc-iq.csv')
        #print('successful')
    elif "AWS::IAM::Role" in restype:
        print ('IAM')    
        
       # iamresponse = role.description(RoleName=physicalresId)
        #dfiam = pd.DataFrame(iamresponse['PolicyNames'])
        #dfiam.to_csv('iam-list-role-iq-'+ physicalresId +'.csv')
        #print(dfiam)
    elif  "AWS::S3::Bucket" in restype:
        #print(restype)
        s3response = S3.list_objects(Bucket=physicalresId)
         
        dfs3 = pd.DataFrame(s3response['ResponseMetadata'])
        dfs3.to_csv('s3-bucket-iq.csv')
        print(s3response)
         
    elif  "AWS::EC2::VPC" in restype:
       vpcresponse = ec2.describe_vpcs(VpcIds=['vpc-010fa25ba11428e17'])
       dfvpc = pd.DataFrame(vpcresponse['Vpcs'])
       dfvpc.to_csv('vpc-describe-iq.csv')
       print ('vpssuccess')
    else:
       print('others')
try:
    response = ec2.describe_instances(InstanceIds=['i-0936a1328e6c786c3'])
  #  print('Success', response)
except ClientError as e:
    print('Error', e)



#f.writerow(["StackName","StackId","LogicalResourceId","PhysicalResourceId","ResourceType","Timestamp","ResourceStatus","ResourceStatusReason","Description"])

#loaded_json = json.loads(rspnse)
#f = csv.writer(open("gxpiqrep.csv", "wb+"))
#f.writerow(["StackName","StackId","LogicalResourceId","PhysicalResourceId","ResourceType","Timestamp","ResourceStatus","ResourceStatusReason","Description"])
#for x in x
#for x in rspnse:
	#print(x, rspnse[x])
 #   print ('i am here' , x)
    #y =  y + str((rspnse[x]))
  #  f.writerow([x["StackName"],x["StackId"],x["LogicalResourceId"],x["PhysicalResourceId"],x["ResourceType"],
   #      x["Timestamp"],x["ResourceStatus"],x["ResourceStatusReason"],x["Description"]
   #           ])
  #  print('successful')
#try:
#S3.put_object(Body=y, Bucket="kinsesisredshift", Key="gxpiqrep.csv")
#print('successful')
#except ClientError as e:
 #   print('Error', e)
#input = open(sys.argv[1])
#data = json.load(rspnse)
#data.open()
#data.close()
#print (data)

#output =csv.writer(sys.stdout)
#output.writerow(data[0].keys())
#for row in data:
 #   output.writerow(row.values())

 
#describe_stacks(StackName='diabetes-immersionday-stack') 
#StackName='diabetes-immersionday-stack',PhysicalResourceId='dd1mq3dczxgr5jn')
 