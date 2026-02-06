from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    site = request.form.get("site")

    if site == "google":
        return redirect("https://www.google.com")
    elif site == "youtube":
        return redirect("https://www.youtube.com")
    elif site == "yahoo":
        return redirect("https://www.yahoo.com")
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
