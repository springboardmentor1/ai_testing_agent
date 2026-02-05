from flask import Flask, request, jsonify
from app.agents.baseline_agent import agent


app = Flask(
    __name__,
    static_folder="../static",
    static_url_path=""
)

@app.route("/")
def home():
    return app.send_static_file("index.html")
