import boto3
from botocore.exceptions import ClientError
import os

def upload_file(file_name, bucket, object_name=None):

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    session = boto3.session.Session()
    s3_client = session.client( 
            service_name='s3',
            aws_access_key_id='HAad8lkA1pVmzfCL',
            aws_secret_access_key='oe776fusct7vt0nhfU6IvTdthGhfsGjs',
            endpoint_url='https://u1.s3api.itschool.cloud'
        )

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

upload_file("./static/photos_2023-04-14_12-05/photo_00001.jpg", 'photos', object_name="photos_2023-04-14_12-05/photo_00001.jpg")