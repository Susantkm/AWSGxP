#!/bin/bash -vx
echo $1
echo $2 
echo $3
echo $4
echo $5
echo $6

echo "print the id:" $1
echo "print the dbid:" $2


#cfnstackname2,rdsphysicalresId, ec2physicalresId,s3physicalresId,vpcphysicalresId

chmod 755  ./iqrpt.sh

aws cloudformation describe-stacks --stack-name $1  --output table >>iq_cfnstack.csv

aws cloudformation describe-stack-resources --stack-name $1  --output table >>iq_stackres.csv

aws rds describe-db-instances --db-instance-identifier $2 --output table >>iq_rdsinstance.csv


aws ec2 describe-instances --instance-ids $3 --output table >>iq_ec2instance.csv


aws ec2 describe-vpcs --vpc-ids $5 --output table >>iq_vpcinstance.csv

zip iqreport_$1.zip iq_*.csv

rm -f iq_cfnstack.csv
rm -f iq_stackres.csv
rm -f iq_rdsinstance.csv
rm -f iq_ec2instance.csv
rm -f iq_vpcinstance.csv


exit 0