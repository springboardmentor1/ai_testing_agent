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
    page_title="AI Test Platform",
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

if "example_text" not in st.session_state:
    st.session_state.example_text = ""


# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("AI Test Platform")

    st.markdown("### Navigate")

    section = st.radio(
        "",
        [
            "Test Execution",
            "Test Reports",
            "Analytics",
            "Logs"
        ]
    )

    st.divider()

    st.markdown("### Settings")

    st.session_state.dark_mode = st.toggle("Dark Mode")

    if st.button("Clear History"):
        st.session_state.reports = []
        st.session_state.counter = 0
        if os.path.exists("history.csv"):
            os.remove("history.csv")
        st.success("History Cleared")

    st.divider()

    st.markdown("### Platform Info")
    st.markdown("AI Test Platform")
    st.markdown("Version 1.0 | Enterprise Edition")
    st.markdown("Powered by Playwright & AI Agent")
    st.caption("Developed for Infosys Springboard Internship")


# ---------------- DARK MODE ----------------
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


# ================= TEST EXECUTION =================
if section == "Test Execution":

    st.title("🤖 AI Web Testing Dashboard")
    st.caption("AI Agent for Automated End-to-End Website Testing Using Natural Language")

    st.divider()

    st.subheader("Test Case Examples")

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Google Search"):
        st.session_state.example_text = "Open google and search for laptops"

    if col2.button("Amazon Product Search"):
        st.session_state.example_text = "Open amazon and search for shoes"

    if col3.button("Flipkart Product Search"):
        st.session_state.example_text = "Open flipkart and search for mobiles"

    if col4.button("Local Login Test"):
        st.session_state.example_text = "Open test page and verify login success"

    colA, colB = st.columns([4, 1])

    with colA:
        instruction = st.text_area(
            "Test Instruction",
            value=st.session_state.example_text,
            placeholder="Example: Open google and search for laptops"
        )

    with colB:
        st.write("")
        st.write("")
        run_clicked = st.button("🚀 Run Test", use_container_width=True)

    if run_clicked:

        if instruction.strip() == "":
            st.warning("Please enter a test instruction.")
        else:
            try:
                st.session_state.counter += 1

                progress = st.progress(0)
                status = st.empty()

                status.info("Parsing instruction...")
                progress.progress(20)

                result = agent.invoke({"input": instruction})
                actions = result["actions"]

                status.info("Generating Playwright script...")
                progress.progress(40)

                script = generate_playwright_script(actions)

                status.info("Executing browser automation...")
                progress.progress(70)

                start_time = time.time()
                execution = run_playwright_test(script)
                end_time = time.time()

                duration = round(end_time - start_time, 2)

                progress.progress(100)
                status.success("Execution completed")

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

                st.divider()

                # RESULT CARD
                st.subheader("Test Result")

                c1, c2, c3 = st.columns(3)

                c1.metric("Steps Executed", len(actions))
                c2.metric("Execution Time", f"{duration} sec")

                if execution["status"] == "PASSED":
                    c3.success("PASSED")
                    st.balloons()
                else:
                    c3.error("FAILED")

                st.divider()

                # STEP TIMELINE
                st.subheader("Execution Timeline")

                for i, step in enumerate(actions, 1):
                    target = step.get("target") or step.get("value") or "N/A"

                    with st.container():
                        st.markdown(f"### Step {i}")
                        st.progress(int((i / len(actions)) * 100))
                        st.write(f"**Action:** {step['action']}")
                        st.write(f"**Target / Query:** {target}")
                        st.divider()

            except Exception as e:
                st.error(f"System Error: {str(e)}")


# ================= TEST REPORTS =================
elif section == "Test Reports":

    st.title("Test Reports")

    if st.session_state.reports:

        df = pd.DataFrame(st.session_state.reports)

        st.subheader("Filter Reports")
        status_filter = st.selectbox(
            "Select Status",
            ["All", "PASSED", "FAILED"]
        )

        if status_filter != "All":
            df = df[df["Status"] == status_filter]

        st.dataframe(df, use_container_width=True, height=500)

        csv = df.to_csv(index=False)
        st.download_button(
            "Download Report CSV",
            csv,
            "test_report.csv"
        )

    else:
        st.info("No reports available.")


# ================= ANALYTICS =================
elif section == "Analytics":

    st.title("Analytics Dashboard")

    if st.session_state.reports:

        df = pd.DataFrame(st.session_state.reports)

        total = len(df)
        passed = len(df[df["Status"] == "PASSED"])
        failed = len(df[df["Status"] == "FAILED"])
        avg_time = round(df["Duration (sec)"].mean(), 2)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Tests", total)
        m2.metric("Passed", passed)
        m3.metric("Failed", failed)
        m4.metric("Avg Execution Time", f"{avg_time} sec")

        st.divider()

        status_counts = df["Status"].value_counts()

        fig = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Test Result Distribution",
            color=status_counts.index,
            color_discrete_map={
                "PASSED": "green",
                "FAILED": "red"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("No analytics data available.")


# ================= LOGS =================
# ================= LOGS =================
elif section == "Logs":

    st.title("Execution Logs & Debug Center")

    if st.session_state.reports:

        df = pd.DataFrame(st.session_state.reports)

        st.subheader("Select Test")

        # Single dropdown (latest first)
        selected_id = st.selectbox(
            "Select Test ID",
            sorted(df["ID"].tolist(), reverse=True)
        )

        use_id = selected_id

        test_data = df[df["ID"] == use_id]

        if not test_data.empty:

            test = test_data.iloc[0]

            st.divider()

            # ================= SUMMARY =================
            st.subheader("Test Execution Summary")

            c1, c2, c3, c4 = st.columns(4)

            c1.metric("Test ID", test["ID"])
            c2.metric("Status", test["Status"])
            c3.metric("Steps Executed", test["Steps"])
            c4.metric("Duration", f"{test['Duration (sec)']} sec")

            st.divider()

            # ================= TEST INFO =================
            st.subheader("Test Information")

            st.write("Instruction:", test["Instruction"])
            st.write("Execution Time:", test["Execution Time"])

            st.divider()

            # ================= EXECUTION TIMELINE =================
            st.subheader("Execution Timeline")

            timeline_steps = [
                "Instruction Parsed by AI Agent",
                "Actions Generated",
                "Playwright Script Created",
                "Browser Launched",
                "Website Actions Executed",
                "Result Verified"
            ]

            for i, step in enumerate(timeline_steps, 1):
                progress = int((i / len(timeline_steps)) * 100)
                st.progress(progress)
                st.write(f"Stage {i}: {step}")

            st.divider()

            # ================= LOG VIEWER =================
            st.subheader("Execution Logs")

            logs = str(test["Logs"]).split("\n")

            for log in logs:

                log = log.strip()

                if log == "":
                    continue

                if "PAGE TITLE" in log:
                    st.success(f"PAGE EVENT → {log}")

                elif "VERIFY RESULT" in log:
                    st.info(f"VERIFICATION → {log}")

                elif "Waiting" in log:
                    st.warning(f"BROWSER WAIT → {log}")

                elif "search" in log.lower() or "open" in log.lower():
                    st.write(f"ACTION → {log}")

                else:
                    st.write(f"INFO → {log}")

            st.divider()

            # ================= ERROR HANDLING =================
            if test["Errors"]:

                st.subheader("Error Logs")
                st.code(test["Errors"])

            # ================= FAILED TEST ANALYZER =================
            if test["Status"] == "FAILED":

                st.subheader("Failure Analysis")

                st.error("AI Debug Suggestions")

                possible_reasons = [
                    "Target element not found on the webpage",
                    "Website layout changed during execution",
                    "Login or input required from user",
                    "Slow page loading caused timeout",
                    "Instruction not fully understood by AI agent"
                ]

                for reason in possible_reasons:
                    st.write("•", reason)

                st.info("Tip: Try running the test again or refine the instruction.")

        else:
            st.warning("Test ID not found")

    else:
        st.info("No execution logs available yet.")
