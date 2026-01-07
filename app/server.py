from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Testing Agent is Running"
