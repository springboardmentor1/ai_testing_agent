from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_instruction():
    instruction = request.json.get("instruction")
    print("Received instruction:", instruction)  # backend proof
    return jsonify({
        "status": "received",
        "instruction": instruction
    })

if __name__ == "__main__":
    app.run(debug=True)
