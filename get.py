import boto3
from botocore.exceptions import ClientError
import os

def get_file(bucket, object_name):
    session = boto3.session.Session()
    s3_client = session.client( 
            service_name='s3',
            aws_access_key_id='HAad8lkA1pVmzfCL',
            aws_secret_access_key='oe776fusct7vt0nhfU6IvTdthGhfsGjs',
            endpoint_url='https://u1.s3api.itschool.cloud'
        )
    response = s3_client.get_object(Bucket=bucket, Key=object_name)
    return(response)

file = get_file('photos', 'README.md')
print(*file['Body'].readlines())



