import os
import datetime
from jinja2 import Environment, FileSystemLoader
import base64
# from xhtml2pdf import pisa

class TestReporter:
    def __init__(self):
        self.report_dir = "reports"
        self.assets_dir = os.path.join(self.report_dir, "assets")
        self.template_dir = "static"   # ← UPDATED

        os.makedirs(self.report_dir, exist_ok=True)
        os.makedirs(self.assets_dir, exist_ok=True)

        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def save_screenshot(self, screenshot_bytes, name="screenshot"):
     encoded = base64.b64encode(screenshot_bytes).decode("utf-8")
     return f"data:image/png;base64,{encoded}"


    def generate_html_report(self, test_name, steps, logs, errors, screenshots, final_status):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        template = self.env.get_template("report_template.html")  # ← loads from static/

        html = template.render(
            test_name=test_name,
            timestamp=timestamp,
            steps=steps,
            logs=logs,
            errors=errors,
            screenshots=screenshots,
            final_status=final_status
        )

        safe_name = test_name.replace(" ", "_")
        safe_time = timestamp.replace(":", "-")
        filename = f"{safe_name}_{safe_time}.html"
        filepath = os.path.join(self.report_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)

        return filepath
    
    # def generate_pdf_report(self, test_name, steps, logs, errors, screenshots, final_status):
    # # First generate HTML
    #  html_path = self.generate_html_report(
    #     test_name, steps, logs, errors, screenshots, final_status
    # )
    #  pdf_path = html_path.replace(".html", ".pdf")

    #  with open(html_path, "r", encoding="utf-8") as html_file:
    #         html_content = html_file.read()
    
    #  with open(pdf_path, "wb") as pdf_file:
    #         pisa.CreatePDF(html_content, dest=pdf_file)
    
    #         return pdf_path

