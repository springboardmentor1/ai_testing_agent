import streamlit as st
import pandas as pd
import os
import time
from datetime import datetime

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ---------------------------
# Setup folders
# ---------------------------
if not os.path.exists("reports"):
    os.makedirs("reports")

if not os.path.exists("logs"):
    os.makedirs("logs")

# ---------------------------
# PDF Generator
# ---------------------------
def generate_pdf(test_id, prompt, test_type, status, details, screenshot_path):
    filename = f"{test_id}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(filepath)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>AI Automation Test Report</b>", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    elements.append(Paragraph(f"<b>Test Case ID:</b> {test_id}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Prompt:</b> {prompt}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Test Type:</b> {test_type}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Status:</b> {status}", styles["Normal"]))
    elements.append(Paragraph(f"<b>Details:</b> {details}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    if os.path.exists(screenshot_path):
        elements.append(Image(screenshot_path, width=5 * inch, height=3 * inch))

    doc.build(elements)
    return filepath

# ---------------------------
# CSV Logger
# ---------------------------
def save_csv_log(data):
    file_path = "logs/test_logs.csv"
    df = pd.DataFrame([data])

    if os.path.exists(file_path):
        df.to_csv(file_path, mode="a", header=False, index=False)
    else:
        df.to_csv(file_path, index=False)

    return file_path

# ---------------------------
# STEALTH DRIVER
# ---------------------------
def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )

    return driver

# ---------------------------
# Automation Logic
# ---------------------------
def run_automation(test_type, prompt, test_id):

    screenshot_path = f"reports/{test_id}.png"
    driver = get_driver()
    wait = WebDriverWait(driver, 15)

    try:
        if test_type == "Open Google":

            driver.get("https://www.google.com")
            time.sleep(2)

            # Wait for search box
            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            search_box.send_keys(prompt)
            time.sleep(1)
            search_box.send_keys(Keys.RETURN)

            time.sleep(3)

            if "sorry" in driver.title.lower():
                status = "FAIL"
                details = "Google CAPTCHA triggered"
            else:
                status = "PASS"
                details = "Google search executed successfully"

        elif test_type == "Open Amazon":

            driver.get("https://www.amazon.in")
            time.sleep(3)

            # Check for traffic page
            if "sorry" in driver.page_source.lower() or "rush hour" in driver.page_source.lower():
                status = "FAIL"
                details = "Amazon blocked automation (Traffic page detected)"
            else:
                search_box = wait.until(
                    EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
                )
                search_box.send_keys(prompt)
                search_box.send_keys(Keys.RETURN)

                time.sleep(3)
                status = "PASS"
                details = "Amazon search executed successfully"

        elif test_type == "Open YouTube":

            driver.get("https://www.youtube.com")
            time.sleep(3)

            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )

            search_box.send_keys(prompt)
            search_box.send_keys(Keys.RETURN)

            time.sleep(3)
            status = "PASS"
            details = "YouTube search executed successfully"

        elif test_type == "Open GitHub":

            driver.get("https://github.com")
            time.sleep(3)

            search_box = wait.until(
                EC.presence_of_element_located((By.NAME, "q"))
            )

            search_box.send_keys(prompt)
            search_box.send_keys(Keys.RETURN)

            time.sleep(3)
            status = "PASS"
            details = "GitHub search executed successfully"

        else:
            status = "FAIL"
            details = "Unsupported Test Type"

        driver.save_screenshot(screenshot_path)

    except Exception as e:
        status = "FAIL"
        details = str(e)
        driver.save_screenshot(screenshot_path)

    finally:
        driver.quit()

    return status, details, screenshot_path

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AI Testing Agent", layout="wide")
st.title("🚀 AI Automation Testing Dashboard")

page = st.sidebar.selectbox("Navigate", ["Run Test", "View Logs"])

# ---------------------------
# Run Test Page
# ---------------------------
if page == "Run Test":

    test_type = st.selectbox(
        "Select Test Type",
        ["Open Google", "Open Amazon", "Open YouTube", "Open GitHub"]
    )

    prompt = st.text_input("Enter search keyword")

    if st.button("Run Test"):

        if not prompt:
            st.warning("Enter a search keyword.")
        else:
            test_id = f"TC_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            status, details, screenshot_path = run_automation(
                test_type, prompt, test_id
            )

            if status == "PASS":
                st.success(f"Test ID: {test_id} | Status: {status}")
            else:
                st.error(f"Test ID: {test_id} | Status: {status}")

            st.info(details)

            if os.path.exists(screenshot_path):
                st.image(screenshot_path, use_container_width=True)

            log_data = {
                "Test ID": test_id,
                "Timestamp": datetime.now(),
                "Prompt": prompt,
                "Test Type": test_type,
                "Status": status,
                "Details": details
            }

            csv_path = save_csv_log(log_data)
            pdf_path = generate_pdf(
                test_id, prompt, test_type, status, details, screenshot_path
            )

            col1, col2 = st.columns(2)

            with col1:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "Download PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )

            with col2:
                with open(csv_path, "rb") as f:
                    st.download_button(
                        "Download CSV Logs",
                        data=f,
                        file_name="test_logs.csv",
                        mime="text/csv"
                    )

# ---------------------------
# View Logs Page
# ---------------------------
elif page == "View Logs":

    log_file = "logs/test_logs.csv"

    if os.path.exists(log_file):
        df = pd.read_csv(log_file)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No logs available yet.")
