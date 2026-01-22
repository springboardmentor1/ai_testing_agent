from flask import Flask, request, jsonify
from app.agents.llm_instruction_parser import llm_parser_agent

app = Flask(
    __name__,
    static_folder="../static",
    static_url_path=""
)

# ---- Serve UI ----
@app.route("/")
def home():
    return app.send_static_file("index.html")

# ---- LLM Parser API ----
@app.route("/parse", methods=["POST"])
def parse_instruction():
    data = request.get_json()
    instruction = data.get("instruction")

    result = llm_parser_agent.invoke({
        "input": instruction
    })

    return jsonify({
        "input": result["input"],
        "actions": result["actions"]
    })
