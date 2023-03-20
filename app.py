import shutil
import os
from PIL import Image
print ('Введите имя папки с фотографиями')
input_dir_name = input()
photos = os.listdir(path='./' + input_dir_name)

import datetime
dt_now = datetime.datetime.now()
dt_now_str = str(dt_now)

now = dt_now_str.split(' ')[0]+'_'+dt_now_str.split(' ')[1].split(':')[0]+'-'+dt_now_str.split(' ')[1].split(':')[1]

os.mkdir('photos_'+ now) 
os.mkdir('icons_'+ now)

number = 1
for photo in photos:
    old_address_photo = './' + input_dir_name + '/' + photo
    ext = photo.split('.')[-1]
    shutil.copyfile(old_address_photo, 'photos_'+ now + '/' + 'photo_' + str(number) + '.' + ext)
    
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
    out.save('icons_'+ now + '/' + 'icon_' + str(number) + '.' + ext)

    number += 1
