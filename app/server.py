from flask import Flask, request, jsonify
from instruction_parser.parser import parse_instruction

app = Flask(__name__)


@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json()
    instruction = data.get("instruction")

    result = parse_instruction(instruction)
    return jsonify(result.dict())
