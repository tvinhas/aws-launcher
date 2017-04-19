cassandra-cluster
========

Python script to launch and fully configure a Cassandra cluster on AWS

Important
--------------

Make sure you have the python modules boto3, json and argparse
To install type "pip install module-name" 

- Download the file cassandra-launcher.py from this repository
- Edit the file and add the proper AWS Credentials
- Upload the userdata script to a S3 bucket
- Change the path for the S3 bucket that contains the userdata script
- Run the application by typing "python cassandra-launcher.py"

