import shutil
import os
from PIL import Image
from flask import Flask, send_from_directory, render_template
import datetime

app = Flask(__name__)

@app.route('/statiс/<path:path>')
def static1(path):
    return send_from_directory('static', path)

@app.route("/")
def hello():  
    html = render_template("index.html")
    return html


def make_galery():
    input_dir_name = 'images'
    photos = os.listdir(path = input_dir_name)

    dt_now = datetime.datetime.now()
    dt_now_str = str(dt_now)

    now = dt_now_str.split(' ')[0]+'_'+dt_now_str.split(' ')[1].split(':')[0]+'-'+dt_now_str.split(' ')[1].split(':')[1]

    os.mkdir('static/photos_'+ now) 
    os.mkdir('static/icons_'+ now)

    all_params = []
    number = 1
    icons = []

    for photo in photos:
        old_address_photo = input_dir_name + '/' + photo
        ext = photo.split('.')[-1]
        new_address_photo = 'static/photos_'+ now + '/' + 'photo_' + str(number) + '.' + ext
        shutil.copyfile(old_address_photo, new_address_photo)

        #request = "INSERT INTO `photos` (`folder`, `file`, `user_folder`, `user_file`, `tags`, `comment`)
        # params = ('photoDDMMYYYY', 'photo1', 'My photos', 'mum.png', None, None) 
        temp_dict = {}
        temp_dict['folder'] = 'photos_'+ now
        temp_dict['file'] = 'photo_' + str(number) + '.' + ext
        temp_dict['user_folder'] = input_dir_name
        temp_dict['user_file'] = photo
        temp_dict['tags'] = None
        temp_dict['comment'] = None
        all_params.append(temp_dict)

     
        #read the image 
        im = Image.open(old_address_photo) 

        width = im.size[0] 
        height = im.size[1] 

        #image size
        icon_width = 100 
        size=(icon_width,int(icon_width*height/width)) 

        #resize image 
        out = im.resize(size) 

        #save resized image 
        icon_name = 'static/icons_'+ now + '/' + 'icon_' + str(number) + '.' + ext
        out.save(icon_name)
        icons.append(icon_name)

        number += 1
    
    html = render_template("index.html", icons = icons)
    return html



'''

print (all_params)

import mysql.connector

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

    #здесь один запрос, но их надо отправлять в цикле
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

         # Это завершение работы с БД и сохранение изменений
    connection.commit()

requests_to_db(all_params)
'''


if __name__ == "__main__":
    app.run('0.0.0.0', 3020, debug = True)


