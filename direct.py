import shutil
import boto3
from botocore.exceptions import ClientError
import os
import io
from flask import Flask, send_from_directory, render_template, make_response
from PIL import Image 

app = Flask(__name__)

session = boto3.session.Session()
s3_client = session.client( 
        service_name='s3',
        aws_access_key_id='HAad8lkA1pVmzfCL',
        aws_secret_access_key='oe776fusct7vt0nhfU6IvTdthGhfsGjs',
        endpoint_url='https://u1.s3api.itschool.cloud'
    )

def get_file(bucket, object_name):
    response = s3_client.get_object(Bucket=bucket, Key=object_name)
    response = response["Body"]
    return response

@app.route("/s3/1")
def S3():
    obj = get_file('photos', "photos_2023-04-14_12-05/photo_00001.jpg")

    with io.FileIO('test.jpg', 'w') as file:
        for i in obj:
            file.write(i)

    html = '<img src="/static/test.jpg" width=600>'
    return html


@app.route("/direct/<file>")
def direct_file(file):
    object_name = "/static/photos_2023-04-27_07-19/photo_00002.jpg"
    response_s3 = s3_client.get_object(Bucket='photos', Key=object_name)
    response_s3_body = response_s3["Body"]

    response = make_response(response_s3_body)
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='123.jpg')
    return response

    #response = response["Body"]

    #return html


@app.route("/view")
def view():
    return '<img width=800 src="/direct/1">'



if __name__ == "__main__":
    app.run('0.0.0.0', 3020, debug = True) 