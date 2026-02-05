from flask import Flask, request, jsonify, send_from_directory
from app.agents.instruction_parser_graph import instruction_parser_agent

app = Flask(__name__, static_folder="../../static")


# ----------------------------
# Serve Frontend
# ----------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


# ----------------------------
# Health Check
# ----------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ----------------------------
# Instruction Parser API
# ----------------------------
@app.route("/parse", methods=["POST"])
def parse_instruction():
    """
    Expected JSON:
    {
        "instruction": "open Google and search for Amazon"
    }
    """

    data = request.get_json(silent=True)

    if not data or "instruction" not in data:
        return jsonify({
            "error": "Missing 'instruction' field"
        }), 400

    instruction = data["instruction"]

    # Invoke LangGraph agent
    result = instruction_parser_agent.invoke({
        "input": instruction
    })

    return jsonify(result), 200
