from flask import Flask, render_template

app = Flask(__name__, template_folder="../templates")

@app.route("/")
def home():
    return "AI Testing Agent Server Running"

@app.route("/login")
def login():
    return render_template("test_form.html")

if __name__ == "__main__":
    app.run(debug=True)
