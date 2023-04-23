import shutil
import os
from PIL import Image
from flask import Flask, send_from_directory, render_template 
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

@app.route("/full_size/<photo_id>", methods=['GET'])
def show_photo(photo_id):
    url = get_url(photo_id)
    html = render_template("full_size.html", photo_id=photo_id, url=url) 
    return html  

def get_url(number):
    folders = os.listdir(path = 'static')
    folders.sort()
    photo_folder = folders[1]
    photo_list = os.listdir(path = 'static/' + photo_folder)
    photo_list.sort()
    url =  '../static/' + photo_folder + '/' + photo_list[int(number)-1]
    return url
    
def str_0(number):
    dop = 5 - len(str(number))
    return('0'*dop + str(number))

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
        shutil.copyfile(old_address_photo, new_address_photo)

        #request = "INSERT INTO `photos` (`folder`, `file`, `user_folder`, `user_file`, `tags`, `comment`)
        # params = ('photoDDMMYYYY', 'photo1', 'My photos', 'mum.png', None, None) 
        temp_dict = {}
        temp_dict['folder'] = 'photos_'+ now
        temp_dict['file'] = 'photo_' + str_0(number) + '.' + ext
        temp_dict['user_folder'] = input_dir_name
        temp_dict['user_file'] = photo
        temp_dict['tags'] = None
        temp_dict['comment'] = None
        all_params.append(temp_dict)

        icon = resize_image(old_address_photo, '100', 's')
        #save resized image 
        icon_name = 'static/icons_'+ now + '/' + 'icon_' + str_0(number) + '.' + ext
        icon.save(icon_name)
        icons.append(icon_name)

        sleep(0.5)
        number += 1 

    #print (all_params)
    #requests_to_db(all_params) 
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


def connection_db():
    try:
        db_connection = mysql.connector.connect(

            host="mysql.s1.users24.com",
            port="30096",
            user="root",
            password = 'lkjsfdjklds3248723487BNXNVKHVHweoiwgiwelklkwdsqpsdkfljdls',
            database="masha_photos"
        )    
    except Exception as e:
        print(str(e))

    return db_connection

def requests_to_db(params=None): 
    connection = connection_db()

    mycursor = connection.cursor(dictionary=True)

    for param in all_params:

        folder = param['folder']
        file_name = param['file']
        user_folder = param['user_folder']
        user_file = param['user_file']
        tags = param['tags']
        comment = param['comment']


        request = "INSERT INTO `photos` (`folder`, `file`, `user_folder`, `user_file`, `tags`, `comment`) VALUES (%s, %s, %s, %s, %s, %s);"
        params = (folder, file_name, user_folder, user_file, tags, comment)
    
        mycursor.execute(request, params)

    connection.commit()     

if __name__ == "__main__":
    app.run('0.0.0.0', 3020, debug = True)




