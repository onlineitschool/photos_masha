from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    html = render_template("index.html")
    return html

if __name__ == "__main__":
    app.run('0.0.0.0', 3010, debug = True)