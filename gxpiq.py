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

dfsum = pd.DataFrame()
def writesummary(origsummary):
    
     dfsum = pd.DataFrame(origsummary) 
     dfsum.to_csv('iq-summary-stack.csv')
     print ("successful")
     #for (rtype,count) in origsummary.items():
         #   rcount = list(count)
            
         #   print( "Count for :",rtype,":",rcount[i])
# create zip package out of csv files
def zipthefile(files):
    zipped_file = io.BytesIO()
    with zp.ZipFile(zipped_file, 'w') as f:
        for z, file in enumerate(files):
            f.writestr("{}.csv".format(z), file.getvalue())
            zipped_file.seek(0)
        return outfile.getvalue()           
#role = iam.Role()

if __name__ == '__main__':
    # To get cloudformation status with input, output, tags etc
    #session = boto3.Session(
    #aws_access_key_id='AKIAIWTXRODG2ZBYDKOA',
    #aws_secret_access_key='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')

    #print  ("Region is:", ec2.describe_regions())
    cfn = boto3.client('cloudformation',region_name='us-west-2')
    s3 = boto3.client('s3',region_name='us-west-2')
    ec2 = boto3.client('ec2',region_name='us-west-2')
    rds = boto3.client('rds',region_name='us-west-2')
    kin = boto3.client('kinesis')
    iam = boto3.resource('iam')
    lam=  boto3.client('lambda')
    #role = iam.Role()
       
    cfnstackname2 = 'Data-lake-foundation'
    
    Filter = ['CREATE_COMPLETE','UPDATE_COMPLETE']
    rsp =  cfn.list_stacks(StackStatusFilter=Filter)   
    
    dflist =  pd.DataFrame(rsp['StackSummaries'])

   
     
    dfa = pd.DataFrame()
    dfr = pd.DataFrame()
    dfvpca = pd.DataFrame()
    dfiama = pd.DataFrame()
    dfs3a = pd.DataFrame()
    dfec2a = pd.DataFrame()
    dfrdsa = pd.DataFrame()
    dfkina = pd.DataFrame()
    dforiglista = pd.DataFrame()

    origs3cnt = 0
    origiamnrolecnt = 0

    dfstk = dflist['StackName']
    dflist.to_csv('iq-list-stacks.csv')
    #print (dfstk)
    stkname = list(dflist['StackName'])
    #print ("Stackne name is:",stkname)
    cnt =0
    icount =0
    for stname in stkname:
            
            rspnse =  cfn.describe_stacks(StackName=stname)   
            df = pd.DataFrame(rspnse['Stacks'])
            
            cfnresp = cfn.get_template_summary(StackName=stname)
           #print (cfnresp)
            dftemplate = pd.DataFrame(cfnresp['ResourceTypes'])
            icount = icount+1  
            #print ("response for:",stname, " is: ", df )  
            if icount != 1:
               dforiglista = dforiglista.append(dftemplate)
             

            rspnse11 =  cfn.describe_stack_resources(StackName=stname)   
            df11 = pd.DataFrame(rspnse11['StackResources'])
            cnt = cnt+1  
            #print ("response for:",stname, " is: ", df )  
            if cnt != 1:
                 
                dfa = dfa.append(df)
                
                dfr = dfr.append(df11)
                #print("append is: ",dfr)
    dfa.to_csv('iq-cfn-descstacks-iq.csv')
    dfr.to_csv('iq-resource-stacks-iq.csv')
    dforiglista.to_csv('iq-cfn-template-resource.csv')
           # print("count is", cnt)
            
    rdsphysicalresId =''
    s3physicalresId = ''
    vpcphysicalresId =''
    ec2physicalresId = []

    origrdscount = 0
    origec2count = 0
    origvpccount = 0
    origs3count = 0
    origiamcount = 0
    origlambdacount =0
    origkincount   = 0
    
    rdscount = 0
    ec2count = 0
    vpccount = 0
    s3count = 0
    iamcount = 0
    lambdacount =0
    kincount   = 0
    #read the original source file to get resource type and count
    orig_csv_file = 'iq-cfn-template-resource.csv'
    origcsvReader = pd.read_csv(orig_csv_file)

    for j in  origcsvReader.index:
        origrestypes = origcsvReader['0'][j]
        if    "AWS::RDS::DBInstance" in origrestypes:
                origrdscount = origrdscount + 1
        elif   "AWS::Lambda::Function" in  origrestypes:
                origlambdacount = origlambdacount + 1
                 
        elif   "AWS::IAM::Role" in origrestypes:
                origiamcount = origiamcount + 1
                 
        elif   "AWS::S3::Bucket"  in origrestypes:
                origs3count = origs3count + 1
        elif    origrestypes == "AWS::EC2::Instance":
                origec2count = origec2count + 1
        elif   origrestypes  == "AWS::EC2::VPC":
                origvpccount = origvpccount + 1
        elif  "AWS::KinesisFirehose::DeliveryStream" in origrestypes:
                origkincount = origkincount + 1

    #read the resource stack output csv file to get resource type and Physical resource ID
    csv_file = 'iq-resource-stacks-iq.csv'
    csvReader = pd.read_csv(csv_file)
    fieldnames = ['PhysicalResourceId','ResourceType','StackId']
    csvReader1 = csvReader[fieldnames]
    
    # loop to get each record for resource type and Physical resource ID and then get instance description
    dfrsa = pd.DataFrame()

    for i in  csvReader.index:
        restype = csvReader['ResourceType'][i]
        physicalresId = csvReader['PhysicalResourceId'][i]
        logResourceId = csvReader['StackId'][i]
        #print(physicalresId)
        if "AWS::RDS::DBInstance" in restype:
           # print ('rds is dd1mq3dczxgr5jn', physicalresId)
           rdsresponse = rds.describe_db_instances(DBInstanceIdentifier=physicalresId)
           dfrds = pd.DataFrame(rdsresponse['DBInstances'])
           dfrdsa = dfrdsa.append(dfrds)
           dfrdsa.to_csv('iq-rds-dbinstancedesc.csv')

           rdsphysicalresId = physicalresId
           rdscount = rdscount +1  
        elif  "AWS::Lambda::Function" in  restype:
            #lamresp = lam.describe_delivery_stream(DeliveryStreamName='string')
            lambdacount = lambdacount + 1

        elif "AWS::KinesisFirehose::DeliveryStream" in  restype:
            kincount = kincount + 1
        #    print(physicalresId)
        #    kinresp = kin.describe_stream_summary(StreamARN=logResourceId)
        #    dfkin = pd.DataFrame(ec2response['StreamDescriptionSummary'])
        #    dfkina = dfkina.append(dfkin)
        #    dfkina.to_csv('iq-kinesis-descsummary.csv')
        #    print (kinresp)

        elif  "AWS::EC2::Instance" in restype:
            ec2physicalresId = physicalresId
            ec2count = ec2count + 1
            ec2response = ec2.describe_instances(InstanceIds=[physicalresId])
            #print (ec2response) 
            dfec2 = pd.DataFrame(ec2response['Reservations'])
            dfec2a = dfec2a.append(dfec2)
            dfec2a.to_csv('iq-ec2-instancedesc.csv')
                #print('EC2 successful')

        elif "AWS::IAM::Role" == restype:
            role = iam.Role(physicalresId)
            iamroleresp = role.get_available_subresources()
            dfiam = pd.DataFrame(iamroleresp)
            dfiama = dfiama.append(dfiam)
            dfiama.to_csv('iq-iamrole-describe.csv')
            iamcount = iamcount + 1
            #print (iamroleresp)
             
            
        elif  "AWS::S3::Bucket" in restype:
            #s3bucklcl = s3.BucketLifecycle(physicalresId)
            s3physicalresId = physicalresId            
            s3count = s3count + 1
            #dfs3resp = s3bucklcl.get_available_subresources()
            #dfs3 = pd.DataFrame(dfs3resp)
            #dfs3a = dfs3a.append(dfs3)
            #dfvpca.to_csv('siq-3-describe.csv')
            #print("bucket lifecycle: ", bucket_lifecycle)
            
        elif  "AWS::EC2::VPC" == restype:
            vpccount = vpccount + 1
            vpcphysicalresId= physicalresId
            vpcresponse = ec2.describe_vpcs(VpcIds=[physicalresId])
            dfvpc = pd.DataFrame(vpcresponse['Vpcs'])
            dfvpca = dfvpca.append(dfvpc)
            dfvpca.to_csv('iq-vpc-describe.csv')
            #print(vpc)
            #dfvpc = pd.Dataframe(vpcresp)
        
        else: continue
    
    summary ={"IAM":[iamcount, origiamcount],
                  "EC2":[ec2count, origec2count],
                  "VPC":[vpccount, origvpccount],
                  "S3":[s3count, origs3count],
                  "Kinesis":[kincount, origkincount],
                  "DBInstance":[rdscount, origrdscount],
                  "Lambda":[lambdacount, origlambdacount]
                  } 
    #print("summary is:", summary)              
    writesummary(summary)
    stackn = "DataLake-Stack"
    #Calling iqrpt.sh to create the output files
    status = sub.call(['./iqrpt.sh', stackn])

    #files = [('iq-list-stacks.csv',dflist),
    #        ('iq-cfn-descstacks-iq.csv',dfa),
    #        ('iq-resource-stacks-iq.csv',dfr),
    #        ('iq-cfn-template-resource.csv',dforiglista),
    #        ('iq-rds-dbinstancedesc.csv',dfrdsa),
    #        ('iq-ec2-instancedesc.csv',dfec2a),
    #        ('iq-iamrole-describe.csv',dfiama),
    #        ('iq-vpc-describe.csv',dfvpca),
    #        ('iq-summary-stack.csv',dfsum)
    #        ]
    #zpfile = zipthefile(files)


    #Calling iqrpt.sh to create the output files
    #status = sub.call(['./iqrpt.sh', cfnstackname2, str(rdsphysicalresId), str(ec2physicalresId), str(s3physicalresId), str(vpcphysicalresId),str(rdscount),str(ec2count),str(s3count),str(vpccount)])

    #status = sub.call(['./iqrpt.sh', cfnstackname2, rdsphysicalresId, ec2physicalresId, s3physicalresId, vpcphysicalresId,])


    #os.remove("resource-stacks-iq.csv")
    #print("successful removing the temp excel file")

    #status = zipthefile()

    #print( status)