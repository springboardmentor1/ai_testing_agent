from flask import Flask, request, jsonify
from app.agents.baseline_agent import agent
from app.agents.playwright_generator import generate_playwright_script
from app.agents.playwright_executor import run_playwright_test


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

    result = agent.invoke({"input": instruction})
    actions = result["actions"]

    script = generate_playwright_script(actions)
    execution = run_playwright_test(script)

    return jsonify({
        "instruction": instruction,
        "actions": actions,
        "script": script,
        "execution": execution
    })