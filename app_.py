from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/statiс/<path:path>')
def static1(path):
    return send_from_directory('static', path)

@app.route("/")
def hello():
    return "<p>hello</p>"

if __name__ == "__main__":
    app.run('0.0.0.0', 3010, debug = True)