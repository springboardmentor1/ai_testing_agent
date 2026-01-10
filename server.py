# from flask import Flask, request, jsonify  
# import os

# current_dir = os.path.dirname(os.path.abspath(__file__))

# static_path = os.path.join(current_dir, "static")


# app = Flask(
#     __name__,
#     static_folder=static_path,
#     static_url_path="")

# @app.route("/")
# def home():
#     return app.send_static_file("index.html")

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

from flask import Flask, request, jsonify
from agents.baseline_agent import agent # This imports your compiled graph
import os

app = Flask(__name__, static_folder="static", static_url_path="")

@app.route("/")
def home():
    return app.send_static_file("index.html")

# NEW: API Endpoint to make user input dynamic
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    
    # Trigger your LangGraph agent dynamically
    # This matches the .invoke() logic in your testing.py
    result = agent.invoke({"input": user_message})
    
    return jsonify({"status": "success", "response": result["output"]})

if __name__ == "__main__":
    app.run(debug=True, port=5000)