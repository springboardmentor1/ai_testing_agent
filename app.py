'''import gradio as gr
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
        share=True,
        css=custom_css,
        theme=gr.themes.Soft(),
        show_error=True
    )'''

import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from instruction_parser import agent
from executor import execute_test
import os
import json

HISTORY_FILE = "test_history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(data):
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Test Automation", layout="wide")

# ------------------ CLEAN CSS ------------------
st.markdown("""
<style>
            /* 🔝 TOP NAVBAR BACKGROUND */
header[data-testid="stHeader"] {
    background: linear-gradient(90deg, #e6d8cc, #b89284);
}

/* OPTIONAL: REMOVE SHADOW */
header[data-testid="stHeader"] {
    box-shadow: none !important;
}
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Poller+One&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Marcellus&family=Orbitron:wght@400;700&family=Poller+One&display=swap');
/* 🌿 FULL PAGE BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(90deg, #e6d8cc, #b89284);

/* REMOVE DEFAULT LAYERS */
section.main > div {
    background: transparent !important;
}

/* 🧊 CARD (MATCHING GRADIENT, NO WHITE) */
.block-container {
    background: linear-gradient(90deg, #e6d8cc, #b89284);
    border-radius: 20px;
    padding: 2rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        
}

table {
    border-collapse: collapse !important;
    width: 50%;
}

/* Table borders */
th, td {
    border: 2px solid #5e3b2e !important;   /* thicker + visible */
    padding: 10px;
}

/* Header styling */
th {
    background-color: rgba(255,255,255,0.4) !important;
    font-weight: bold;
    color: #5e3b2e !important;
}

/* Row hover (optional cool effect) */
tr:hover {
    background-color: rgba(255,255,255,0.3);
}
.tagline {
    font-family: 'Orbitron', sans-serif !important;
    text-align: center;
    color: #5e3b2e;
    font-size: 22px;
    letter-spacing: 5px;
    margin-top: -10px;
            font-weight: 700;
}

/* ✍️ INPUT */
textarea {
    background: linear-gradient(90deg, #e6d8cc, #b89284);
    border: 2px solid #5e3b2e !important;
    border-radius: 10px;
}

/* 🚀 BUTTON */
.stButton>button {
    background: #b08968;
    color: black;
    border-radius: 12px;
    height: 3em;
    font-weight: 500;
}

h1 {
            font-family: 'Orbitron', 'Poller One', sans-serif !important;
    letter-spacing: 2px;
    font-weight: 700;
            color: #5e3b2e !important; 
            font-size: 4em !important;
            /* deep teal */
}

h2, h3 {
            font-family: 'Marcellus', serif !important;
    letter-spacing: 1px;
    color: #5e3b2e !important; 
            font-size: 1.25em !important;
            /* rich blue */
}
/* 🎯 CENTER METRIC VALUES */
div[data-testid="metric-container"] {
    text-align: center !important;
}

/* CENTER LABEL (Total, Passed, Failed) */
div[data-testid="metric-container"] label {
    justify-content: center !important;
    width: 100%;
}

/* CENTER NUMBER */
div[data-testid="metric-container"] div {
    justify-content: center !important;
}
            /* 📜 EXPANDER (View Logs) */
div[data-testid="stExpander"] {
    background: transparent !important;
    border: 1px solid #7f5539;
    border-radius: 10px;
}

/* JSON BOX */
div[data-testid="stJson"] {
    background: rgba(255,255,255,0.2) !important;
    border-radius: 10px;
}

/* CODE BLOCK INSIDE JSON */
pre {
    background: rgba(255,255,255,0.2) !important;
    color: #3e2723 !important;
}

/* 📊 DATAFRAME (HISTORY TABLE) */
div[data-testid="stDataFrame"] {
    background: transparent !important;
}

/* TABLE INSIDE DATAFRAME */
div[data-testid="stDataFrame"] table {
    background: rgba(255,255,255,0.2) !important;
    border-radius: 10px;
}

/* HEADERS */
div[data-testid="stDataFrame"] th {
    background: rgba(255,255,255,0.3) !important;
    color: #5e3b2e !important;
}

/* ROWS */
div[data-testid="stDataFrame"] td {
    background: rgba(255,255,255,0.15) !important;
}

/* DOWNLOAD BUTTON */
.stDownloadButton button {
    background: #b08968 !important;
    color: black !important;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
# ------------------ PDF FUNCTION ------------------
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

# ------------------ RUN TEST ------------------
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
            "steps_executed": 0,
            "error": str(e)
        }

        pdf_path = save_pdf(error_report)
        return error_report, pdf_path

# ------------------ UI ------------------

st.markdown("<center><h1>🤖TestFlow AI</h1></center>", unsafe_allow_html=True)
st.markdown("""
<p class="tagline">
Automate testing with intelligence..🌟
            <br/>
            <br/>
</p>
""", unsafe_allow_html=True)

# 📊 Test Summary (CENTERED PROPERLY)

st.markdown(
    "<h2 style='text-align:center;'>📊 Test Summary</h2>",
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    history = load_history()

    total = len(history)
    passed = sum(1 for h in history if h.get("status") == "PASS")
    failed = sum(1 for h in history if h.get("status") == "FAIL")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("<h4 style='text-align:center;color: #5e3b2e;'>Total</h4>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{total}</h2>", unsafe_allow_html=True)

    with c2:
        st.markdown("<h4 style='text-align:center;color: #5e3b2e;   '>Passed</h4>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{passed}</h2>", unsafe_allow_html=True)

    with c3:
        st.markdown("<h4 style='text-align:center;color: #5e3b2e;'>Failed</h4>", unsafe_allow_html=True)
        st.markdown(f"<h2 style='text-align:center;'>{failed}</h2>", unsafe_allow_html=True)
# 📋 Test Suite
st.markdown("""
<h2 style='text-align:center;'> <br/>
📋 Predefined Test Suite (Expected Outcomes)
</h2>
""", unsafe_allow_html=True)



test_suite_data = [
    {"Test Case": "Open linkedin.com", "Expected Result": "PASS"},
    {"Test Case": "Open google and open amazon.in", "Expected Result": "PASS"},
    {"Test Case": "Open amazon.in and search for phone", "Expected Result": "PASS"},
    {"Test Case": "Login and verify dashboard", "Expected Result": "PASS"},
    {"Test Case": "Open invalidsite123.com", "Expected Result": "FAIL"},
    {"Test Case": "Search invalid input", "Expected Result": "FAIL"},
]

df = pd.DataFrame(test_suite_data)

# ✅ IMPORTANT CHANGE HERE
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.table(df)  # instead of st.dataframe()

st.markdown("---")
st.markdown("""
<div style="
    max-width: 700px;
    margin: auto;
">
""", unsafe_allow_html=True)
# 🧪 Run Test
st.subheader("🔍 Run a Test Case")

test_input = st.text_area("Enter test case here...")

if st.button("🚀 Run Test"):

    if test_input:
        with st.spinner("Running AI Test... 🤖"):
            report, pdf_path = run_test_case(test_input)
            history = load_history()
            history.append(report)
            save_history(history)

        if report.get("status") == "PASS":
            st.success("✅ Test Passed")
        else:
            st.error("❌ Test Failed")

        st.info(f"Steps Executed: {report.get('steps_executed', 0)}")

        with st.expander("📜 View Execution Logs"):
            st.json(report)

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download PDF Report",
                f,
                file_name="test_report.pdf"
            )

    else:
        st.warning("⚠️ Please enter a test case")
st.markdown("## 📜 Test History")

history = load_history()

if history:
    df_history = pd.DataFrame(history)
    st.dataframe(df_history, use_container_width=True)
else:
    st.info("No test history available.")
if st.button("🗑 Clear History"):
    save_history([])
    st.success("History cleared!")