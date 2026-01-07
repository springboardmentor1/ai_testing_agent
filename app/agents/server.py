from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="../../static")

@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")
