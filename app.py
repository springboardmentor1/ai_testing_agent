import gradio as gr
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from instruction_parser import agent
from executor import execute_test

#CUSTOM CSS
custom_css = """
body, #root, .app {
    background-color: #B287A3;
}

.gradio-container {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 10px;
    max-width: 950px;
    margin: auto;
    box-shadow: 0 10px 40px rgba(0,0,0,0.2);
}

h1, h2, h3 {
    color: #9E1C60 !important;
    font-weight: 700;
}

table, th, td {
    color: #FF8FB7 !important;
}

thead th {
    background-color: #F6D6E4 !important;
    color: #9E1C60 !important;
}

textarea, input {
    border-color: #E07A9E !important;
    color: #FF8FB7 !important;
}

button {
    background-color: #FF8FB7 !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600;
}

button:hover {
    background-color: #C76586 !important;
}
"""

#TEST SUITE TABLE
test_suite_data = [
    {"Test Case": "Open linkedin.com", "Expected Result": "PASS"},
    {"Test Case": "Open google and open amazon.in", "Expected Result": "PASS"},
    {"Test Case": "Open amazon.in and search for phone", "Expected Result": "PASS"},
    {
        "Test Case": "Open the login page, enter valid username and password, click login and verify the dashboard is displayed",
        "Expected Result": "PASS"
    },
    {"Test Case": "Open invalidsite123.com", "Expected Result": "FAIL"},
    {"Test Case": "Open google and search in non-existing input", "Expected Result": "FAIL"},
]

test_suite_df = pd.DataFrame(test_suite_data)


#CREATE PDF REPORT
def save_pdf(report):
    path = "test_report.pdf"
    c = canvas.Canvas(path, pagesize=letter)
    y = 750

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "AI Test Automation Report")
    y -= 40

    c.setFont("Helvetica", 11)

    for key, value in report.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

    c.save()
    return path


#RUN TEST FUNCTION
def run_test_case(test_case):
    try:
        parser_result = agent.invoke({"input": test_case})
        playwright_json = parser_result["output"]

        report = execute_test(playwright_json, test_case, headless=True)

        pdf_path = save_pdf(report)

        return report, pdf_path

    except Exception as e:
        error_report = {
            "test_case": test_case,
            "status": "FAIL",
            "error": str(e)
        }

        pdf_path = save_pdf(error_report)
        return error_report, pdf_path


#GRADIO UI
with gr.Blocks(title="AI Test Automation Dashboard") as demo:

    gr.Markdown("# 🤖 AI Test Automation Dashboard")

    gr.Markdown("## 📋 Predefined Test Suite (Expected Outcomes)")
    gr.Dataframe(value=test_suite_df, interactive=False)

    gr.Markdown("---")

    gr.Markdown("## 🧪 Run a Test Case")

    test_input = gr.Textbox(
        lines=3,
        placeholder="Enter test case here..."
    )

    run_btn = gr.Button("🚀 Run Test")

    with gr.Group():
        gr.Markdown("## 📊 Execution Report")

        report_output = gr.JSON()
        pdf_file = gr.File(label="⬇️ Download PDF Report")

    run_btn.click(
        run_test_case,
        inputs=test_input,
        outputs=[report_output, pdf_file]
    )

#LAUNCH APP
if __name__ == "__main__":
    demo.launch(
        share=False,
        css=custom_css,
        theme=gr.themes.Soft(),
        show_error=True
    )




