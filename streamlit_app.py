import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px
from datetime import datetime

from app.agents.baseline_agent import agent
from app.agents.playwright_generator import generate_playwright_script
from app.agents.playwright_executor import run_playwright_test


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Web Testing Agent",
    layout="wide",
    page_icon="🤖"
)

# ---------------- SESSION INIT ----------------
if "reports" not in st.session_state:
    if os.path.exists("history.csv"):
        st.session_state.reports = pd.read_csv("history.csv").to_dict("records")
    else:
        st.session_state.reports = []

if "counter" not in st.session_state:
    st.session_state.counter = len(st.session_state.reports)

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙ Settings")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "PASSED", "FAILED"]
    )

    st.session_state.dark_mode = st.toggle("🌙 Dark Mode")

    if st.button("🗑 Clear History"):
        st.session_state.reports = []
        st.session_state.counter = 0
        if os.path.exists("history.csv"):
            os.remove("history.csv")
        st.success("History Cleared!")


# ---------------- DARK MODE STYLE ----------------
if st.session_state.dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0e1117;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ================= MAIN AREA =================

st.title("🤖 AI Web Testing Dashboard")
st.caption("AI Agent for Automated End-to-End Website Testing Using Natural Language")


st.divider()

# -------- TEST CASE EXAMPLES --------
st.subheader("📌 Test Case Examples")

example_cols = st.columns(3)

if example_cols[0].button("Open Google & Search Laptops"):
    st.session_state.example_text = "Open google and search for laptops"

if example_cols[1].button("Search Mobiles on Flipkart"):
    st.session_state.example_text = "Open flipkart and search for mobiles"

if example_cols[2].button("Test Local Login Page"):
    st.session_state.example_text = "Open test page and verify login success"

if "example_text" not in st.session_state:
    st.session_state.example_text = ""


# -------- INPUT SECTION --------
col1, col2 = st.columns([4, 1])

with col1:
    instruction = st.text_area(
        "Test Instruction",
        value=st.session_state.example_text,
        placeholder="Example: Open google and search for laptops"
    )

with col2:
    st.write("")
    st.write("")
    run_clicked = st.button("🚀 Run Test", use_container_width=True)


# ---------------- RUN TEST ----------------
if run_clicked:

    if instruction.strip() == "":
        st.warning("Please enter a test instruction.")
    else:
        try:
            st.session_state.counter += 1

            with st.spinner("Executing test... ⏳"):

                # Parse instruction
                result = agent.invoke({"input": instruction})
                actions = result["actions"]

                # Generate script
                script = generate_playwright_script(actions)

                # Execute and measure time
                start_time = time.time()
                execution = run_playwright_test(script)
                end_time = time.time()

                duration = round(end_time - start_time, 2)

            report = {
                "ID": st.session_state.counter,
                "Instruction": instruction,
                "Steps": len(actions),
                "Duration (sec)": duration,
                "Execution Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": execution["status"],
                "Logs": execution["stdout"],
                "Errors": execution["stderr"]
            }

            st.session_state.reports.append(report)

            pd.DataFrame(st.session_state.reports).to_csv("history.csv", index=False)

            st.success("Test Completed Successfully!")

            st.metric("⏱ Execution Time (Latest Test)", f"{duration} sec")

            with st.expander("🔍 View Parsed Actions"):
                for i, step in enumerate(actions, 1):
                    st.write(f"Step {i}: **{step['action']}** → {step.get('target', '')}")

        except Exception as e:
            st.error(f"System Error: {str(e)}")


# ---------------- DASHBOARD ----------------
if st.session_state.reports:

    df = pd.DataFrame(st.session_state.reports)

    if status_filter != "All":
        df = df[df["Status"] == status_filter]

    total = len(df)
    passed = len(df[df["Status"] == "PASSED"])
    failed = len(df[df["Status"] == "FAILED"])
    latest_duration = df.iloc[-1]["Duration (sec)"]
    avg_duration = round(df["Duration (sec)"].mean(), 2)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Tests", total)
    m2.metric("Passed ✅", passed)
    m3.metric("Failed ❌", failed)
    m4.metric("⏱ Avg Execution Time", f"{avg_duration} sec")

    st.divider()

    st.subheader("📊 Execution Report")

    def highlight_status(val):
        if val == "PASSED":
            return "background-color: #d4edda; color: green; font-weight: bold;"
        elif val == "FAILED":
            return "background-color: #f8d7da; color: red; font-weight: bold;"
        return ""

    styled_df = df.style.applymap(highlight_status, subset=["Status"])

    st.dataframe(styled_df, use_container_width=True, height=400)

    # Download CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name="test_report.csv",
        mime="text/csv"
    )

    st.divider()

    # Analytics
    # Analytics
    st.subheader("📈 Test Analytics")
    status_counts = df["Status"].value_counts()
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Result Distribution",
        color=status_counts.index,
        color_discrete_map={
            "PASSED": "green",
            "FAILED": "red"
    }
)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # Logs
    st.subheader("📝 Latest Test Logs")

    with st.expander("View Execution Logs"):
        st.code(st.session_state.reports[-1]["Logs"])

    with st.expander("View Errors"):
        st.code(st.session_state.reports[-1]["Errors"])
