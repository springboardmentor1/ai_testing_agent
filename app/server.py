from flask import Flask, render_template, request, send_from_directory
from app.utils.report import generate_pdf
import webbrowser
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    status = None
    details = None
    pdf_file = None

    if request.method == "POST":
        prompt = request.form.get("prompt")

        try:
            # Very basic prompt parsing logic
            if "google" in prompt.lower():
                webbrowser.open("https://www.google.com")
                status = "PASS"
                details = "Google opened successfully."

            elif "amazon" in prompt.lower():
                webbrowser.open("https://www.amazon.in")
                status = "PASS"
                details = "Amazon opened successfully."

            else:
                status = "FAIL"
                details = "Unsupported website in prompt."

            pdf_file = generate_pdf(prompt, status, details)

        except Exception as e:
            status = "FAIL"
            details = str(e)

    return render_template(
        "index.html",
        status=status,
        details=details,
        pdf_file=pdf_file
    )

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("static", filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
