from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    instruction = data.get("instruction", "")
    return jsonify({"received_instruction": instruction})

if __name__ == "__main__":
    app.run(debug=True)
