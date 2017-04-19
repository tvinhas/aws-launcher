#!/bin/bash
#####################################################################
# cassandra cluster userdata.sh                                     #
# Developed by Thiago Vinhas                                        #
#                                                                   #
# This script registers the instance to route53 and runs chef       #
#####################################################################

# Gets environmental data
HOST=`aws ec2 describe-tags --region us-east-1 --filters "Name=resource-id,Values=\`curl -s http://169.254.169.254/latest/meta-data/instance-id\`" "Name=key,Values=Name"  | grep Value | awk -F "\"" '{print $4}'`
DOMAIN="vinhas.net"
HOSTNAME=$HOST.$DOMAIN
IPADDR=`ifconfig |grep Bcast| sed s/':'/' '/g | awk {'print $3'}`
ZONEID=`aws route53 list-hosted-zones-by-name --dns-name $DOMAIN | grep hostedzone | awk -F / '{print $3}' | sed s/\",//g`

# Changing hostname to reflect the instance Name tag
echo "preserve_hostname: true" >> /etc/cloud/cloud.cfg
echo "HOSTNAME=$HOSTNAME" >>/etc/sysconfig/network
echo "$HOSTNAME" >/etc/hostname
hostname $HOSTNAME

# Register instance to Route53
    TMPFILE=$(mktemp /tmp/temporary-file.XXXXXXXX)
    cat > ${TMPFILE} << EOF
    {
      "Comment":"Adding instance to route53",
      "Changes":[
        {
          "Action":"UPSERT",
          "ResourceRecordSet":{
            "Name": "$HOSTNAME.",
            "Type": "A",
            "TTL": 300,
            "ResourceRecords":[
              {
                "Value":"$IPADDR"
              }
            ]
          }
        }
      ]
    }
EOF

# Sets up the DNS zones on Route 53 and on the instance
aws route53 change-resource-record-sets --hosted-zone-id $ZONEID --change-batch file://"$TMPFILE"
sleep 30 # Just to make sure we have enough time to propagate the DNS change
sed -i s/ec2.internal/vinhas.net/g /etc/resolv.conf
yum install git -y
git -C /tmp clone https://github.com/tvinhas/cassandra-cluster.git
mv /tmp/cassandra-cluster/chef /etc
rpm -Uvh https://packages.chef.io/stable/el/6/chef-12.11.18-1.el6.x86_64.rpm
chef-solo -c /etc/chef/solo.rb
