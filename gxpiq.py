#!/usr/bin/env python

import sys
import json
import csv
import boto3
import os as os
from botocore.exceptions import ClientError
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import numpy as np
import datetime as dt
import subprocess as sub
import io
import zipfile as zp


cfn = boto3.client('cloudformation')
S3 = boto3.client('s3')
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
iam = boto3.client('iam')
#role = iam.Role()


# To get cloudformation status with input, output, tags etc
cfnstackname2 = 'diabetes-immersionday-stack'

rspnse =  cfn.describe_stacks(StackName=cfnstackname2)   
df = pd.DataFrame(rspnse['Stacks'])

# To get ALl Resource Stacks and their details
rspnse11 =  cfn.describe_stack_resources(StackName=cfnstackname2)   
df11 = pd.DataFrame(rspnse11['StackResources'])
df11.to_csv('resource-stacks-iq.csv')
#writingExcel(filename,sheetname,dfname)

#read the csv file to get resource type and Physical resource ID
csv_file = 'resource-stacks-iq.csv'
csvReader = pd.read_csv(csv_file)
fieldnames = ['PhysicalResourceId','ResourceType']
csvReader1 = csvReader[fieldnames]
# loop to get each record for resource type and Physical resource ID and then get instance description
rdsphysicalresId =''
s3physicalresId = ''
vpcphysicalresId =''
ec2physicalresId = []

files = [('cfnstack.csv',df),('stackres.csv',df11)]
# create zip package out of csv files
def zipthefile():
    zipped_file = io.BytesIO()
    with zp.ZipFile(zipped_file, 'w') as f:
        for i, file in enumerate(files):
            f.writestr("{}.csv".format(i), file.getvalue())
    zipped_file.seek(0)
    return outfile.getvalue()
    

for i in  csvReader.index:
    restype = csvReader['ResourceType'][i]
    physicalresId = csvReader['PhysicalResourceId'][i]
    
    if "AWS::RDS::DBInstance" in restype:
       print ('rds is dd1mq3dczxgr5jn', physicalresId)
       rdsphysicalresId = physicalresId
       
    elif  "AWS::EC2::Instance" in restype:
        ec2physicalresId = physicalresId
        
        print('EC2 successful')

    elif "AWS::IAM::Role" == restype:
        print ('IAM')    
        
    elif  "AWS::S3::Bucket" in restype:
        
        s3physicalresId = physicalresId
        
        print("S3 Successful")
         
    elif  "AWS::EC2::VPC" == restype:
       
        vpcphysicalresId= physicalresId
       
    else: continue
       
#print (cfnstackname2,rdsphysicalresId,ec2physicalresId,s3physicalresId,vpcphysicalresId)

#Calling iqrpt.sh to create the output files
status = sub.call(['./iqrpt.sh', cfnstackname2, rdsphysicalresId, ec2physicalresId, s3physicalresId, vpcphysicalresId])
   #status = subprocess.call(['./iqrpt.sh '])
print('status:', status)

os.remove("resource-stacks-iq.csv")
print("successful removing the temp excel file")

#status = zipthefile()

print( status)






