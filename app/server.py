from flask import Flask, request, jsonify
from app.agents.baseline_agent import agent

app = Flask(
    __name__,
    static_folder="../static",
    static_url_path=""
)

# ---- Serve UI ----
@app.route("/")
def home():
    return app.send_static_file("index.html")

# ---- Parser API (rule + LLM combined) ----
@app.route("/parse", methods=["POST"])
def parse_instruction():
    data = request.get_json()
    instruction = data.get("instruction")

    result = agent.invoke({
        "input": instruction
    })

    return jsonify({
        "input": result["input"],
        "actions": result["actions"]
    })
