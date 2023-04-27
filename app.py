import shutil
import boto3
from botocore.exceptions import ClientError
import os
import io

import time

from flask import Flask, send_from_directory, render_template 

from PIL import Image

from flask import request
import datetime
import mysql.connector

app = Flask(__name__)

@app.route('/statiс/<path:path>')
def static1(path):
    return send_from_directory('static', path)

@app.route("/")
def hello():  
    html = 'hello'
    return html

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

def upload_file(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

# Ask the user about previous uploads and getting the files

# Upload all the files to s3
# Make icons, upload them to s3 and save nearby

def str_0(number):
    dop = 5 - len(str(number))
    return('0'*dop + str(number))

def file_processing():
    input_dir_name = 'images'
    photos = os.listdir(path = input_dir_name)
    print(photos)

    dt_now = datetime.datetime.now()
    dt_now_str = str(dt_now)
    now = dt_now_str.split(' ')[0]+'_'+dt_now_str.split(' ')[1].split(':')[0]+'-'+dt_now_str.split(' ')[1].split(':')[1]

    os.mkdir('static/photos_'+ now) 
    os.mkdir('static/icons_'+ now)
    os.mkdir('static/resized_'+ now)

    all_params = []
    number = 1

    icons = []

    for photo in photos:

        old_address_photo = input_dir_name + '/' + photo
        ext = photo.split('.')[-1]
        new_address_photo = 'static/photos_'+ now + '/' + 'photo_' + str_0(number) + '.' + ext
        # shutil.copyfile(old_address_photo, new_address_photo)
        upload_file(old_address_photo, 'photos', new_address_photo)

        icon = resize_image(old_address_photo, '100', 's')
        #save resized image 
        icon_name = 'static/icons_'+ now + '/' + 'icon_' + str_0(number) + '.' + ext
        icon.save(icon_name)
        icons.append(icon_name)
        upload_file(icon_name, 'photos', icon_name)

        time.sleep(0.1)
        number += 1 

    print(icons)
    return(icons)

def resize_image(old_address_photo, new_width, new_height):

    #read the image 
    im = Image.open(old_address_photo) 

    width = im.size[0] 
    height = im.size[1] 

    #image size
    if new_height == "s" and new_width == "s":
         size=(width, height)

    elif new_height == "s":
        new_width = int(new_width)
        size=(new_width,int(new_width * height/width)) 

    elif new_width == "s":
        new_height = int(new_height)
        size=(int(new_height * width/height), new_height)
    
    else:
        new_width = int(new_width)
        new_height = int(new_height)
        size = (new_width, new_height)

    #resize image 
    out = im.resize(size) 

    return out

# Show icons from nearby

@app.route("/gallery")
def make_gallery():
    print('make gallery')

    folders = os.listdir(path = 'static')
    print(os.listdir(path = 'static'))

    icons = []    

    if (len(os.listdir(path = 'static')) > 0): 
        folders.sort()
        icon_folder = folders[0]
        icon_list = os.listdir(path = 'static/' + icon_folder)
        icon_list.sort()
        for icon in icon_list:
            icon = 'static/' + icon_folder + '/' + icon
            icons.append(icon)

    if (len(os.listdir(path = 'static')) == 0):
        print(os.listdir(path = 'static'))
        icons = file_processing()

    paths = {}
    numbers = {}

    for icon in icons:
        icon_tmp = icon
        numbers[icon] = int(icon_tmp.split('.')[-2].split('_')[-1])
        paths[numbers[icon]] =  icon_tmp.replace('icon', 'photo')

    html = render_template("index.html", icons = icons, numbers = numbers) 
    return html  

# Show full-size file from s3 and save it nearby
# Resize file from nearby, download it to user's computer and upload to s3

@app.route("/full_size/<photo_id>", methods=['GET'])
def show_photo(photo_id):
    url = get_url(photo_id)
    my_file = open(url[3:], "w+")
    s3_url = url[3:]
    obj = get_file('photos', s3_url)

    with io.FileIO(url[3:], 'w') as file:
        for i in obj:
            file.write(i)
       
    html = render_template("full_size.html", photo_id=photo_id, url=url) 
    return html 

def get_url(number):
    folders = os.listdir(path = 'static')
    folders.sort()
    icon_folder = folders[0]
    photo_folder = folders[1]
    icon_list = os.listdir(path = 'static/' + icon_folder)
    icon_list.sort()
    icon_url =  '../static/' + photo_folder + '/' + icon_list[int(number)-1]
    photo_url = icon_url.replace("icon", "photo", 1)
    print(photo_url)
    return photo_url
    
@app.route("/resize/<photo_id>", methods=['GET', 'POST'])
def resize(photo_id):
    width = request.form["width"]
    height = request.form["height"]
    if width == '':
        width = "s"
    if height == '':
        height = "s"
    html = resize_photo(photo_id, width, height)
    return html

def resize_photo(photo_id, width, height):

    old_address_photo = get_url(photo_id)[3:]
    ext = old_address_photo.split('.')[-1]

    new_width = width
    new_height = height

    resized = resize_image(old_address_photo, new_width, new_height)

    folders = os.listdir(path = 'static')
    folders.sort()
    resized_folder = folders[2]

    photo_name = "static/" + resized_folder + '/' + 'photo' + str(photo_id) + "_" + str(new_width) + '_' + str(new_height)  + '.' + ext

    resized.save(photo_name)

    html = '<img src = "/' + photo_name + '" height="' + str(new_height) + '">'
    return html 

@app.route("/resized/<photo_id>/<width>/<height>", methods=['GET', 'POST'])
def resized(photo_id, width, height):
    html = resize_photo(photo_id, width, height)
    return html


if __name__ == "__main__":
    app.run('0.0.0.0', 3020, debug = True)