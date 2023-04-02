from flask import Flask, send_from_directory, render_template
import datetime
import os

app = Flask(__name__)

@app.route('/statiс/<path:path>')
def static1(path):
    return send_from_directory('static', path)

@app.route("/")
def hello():  
    html = "hello"
    return html

@app.route("/gallery")
def make_gallery():

    folders = os.listdir(path = 'static')
    folders.sort()
    icon_folder = folders[0]
    url = 'static/icons_2023-04-02_16-14'
    icon_list = os.listdir(path = url)
    icons = []

    for icon in icon_list:
        icon_name = url + '/' + icon
        icons.append(icon_name)
        
    html = render_template("index.html", icons = icons)   
    return html    

if __name__ == "__main__":
    app.run('0.0.0.0', 3010, debug = True)   