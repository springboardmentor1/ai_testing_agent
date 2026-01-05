from flask import Flask, request, jsonify  
import os

current_dir = os.path.dirname(os.path.abspath(__file__))

static_path = os.path.join(current_dir, "static")


app = Flask(
    __name__,
    static_folder=static_path,
    static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)