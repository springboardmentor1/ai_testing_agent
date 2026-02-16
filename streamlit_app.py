import streamlit as st
import requests
import pandas as pd

FLASK_API_URL = "http://127.0.0.1:5000/api"

st.set_page_config(page_title="AI QA Agent", layout="wide")
st.title("🤖 AI Quality Assurance Agent")


with st.sidebar:
    st.header("Test History")
    if st.button("Refresh"): st.rerun()
    try:
        history = requests.get(f"{FLASK_API_URL}/history").json()
        for item in history:
            icon = "✅" if item['status'] == "PASSED" else "❌"
            with st.expander(f"{icon} #{item['id']}"):
                st.write(item['instruction'])
    except:
        st.error("Backend Offline")


instruction = st.text_input("Test Instruction", "Navigate to https://www.google.com and type 'artificial intelligence' into search")

if st.button("🚀 Run Test", type="primary"):
    with st.spinner("Running AI Test... (This may take 30 seconds)"):
        try:
            res = requests.post(f"{FLASK_API_URL}/run-test", json={"instruction": instruction})
            if res.status_code == 200:
                report = res.json().get("report", {})
                
                
                c1, c2 = st.columns(2)
                c1.metric("Status", report['status'])
                
                if report['status'] == "PASSED":
                    c1.success("Test Passed!")
                else:
                    c1.error("Test Failed!")
                
                
                st.subheader("Execution Logs")
                for log in report.get("logs", []):
                    msg = log.get("message") if isinstance(log, dict) else str(log)
                    if "success" in str(log).lower():
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
            else:
                st.error("Server Error")
        except Exception as e:
            st.error(f"Connection Failed: {e}")


st.divider()
st.subheader(" Live Report")
try:
    history_data = requests.get(f"{FLASK_API_URL}/history").json()
    if history_data:
        df = pd.DataFrame(history_data)
        display_df = df[['id', 'timestamp', 'instruction', 'status', 'steps_text']]
        display_df.columns = ['ID', 'Time', 'Test Case', 'Status', 'Steps']
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        csv_data = requests.get(f"{FLASK_API_URL}/export").content
        st.download_button("📥 Download Report", csv_data, "report.csv", "text/csv")
except:
    pass