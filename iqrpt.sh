#!/bin/bash -vx
echo $1
echo $2 
echo $3
echo $4
echo $5
echo $6
echo $7
echo $8
echo $9

echo "print the id:" $1
echo "print the dbid:" $2

#now=$(date)

#cfnstackname2,rdsphysicalresId, ec2physicalresId,s3physicalresId,vpcphysicalresId

chmod 755  ./iqrpt.sh

#echo -e  "------IQ Summary  for Resources ----\t Date:\t  $now  \n DB Instances created :\t $6 \n EC2 Instances created :\t $7 \n S3 Buckets created: \t $8 \n No.of VPC created: \t $9 \n"  >>iq_summary.csv


#aws cloudformation describe-stacks --stack-name $1  --output table >>iq_cfnstack.csv

#aws cloudformation describe-stack-resources --stack-name $1  --output table >>iq_stackres.csv

#aws rds describe-db-instances --db-instance-identifier $2 --output table >>iq_rdsinstance.csv


#aws ec2 describe-instances --instance-ids $3 --output table >>iq_ec2instance.csv


#aws ec2 describe-vpcs --vpc-ids $5 --output table >>iq_vpcinstance.csv

zip iqreport_$1.zip iq-*.csv

rm -f iq-cfn-descstacks-iq.csv
rm -f iq-resource-stacks-iq.csv
rm -f iq-cfn-template-resource.csv
rm -f iq-ec2-instancedesc.csv
rm -f iq-vpc-describe.csv
rm -f iq-summary-stack.csv
rm -f iq-iamrole-describe.csv
rm -f iq-list-stacks.csv


exit 0