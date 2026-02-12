import asyncio
import sys
import json
from datetime import datetime


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from agents.baseline_agent import agent


st.set_page_config(
    page_title="Autonomous AI Test Agent", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)


if "report_history" not in st.session_state:
    st.session_state.report_history = []
if "last_run_time" not in st.session_state:
    st.session_state.last_run_time = None


st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; font-weight: bold; }
    .report-card { padding: 1.5rem; border-radius: 10px; background-color: white; border: 1px solid #e1e4e8; margin-bottom: 1rem; }
    .step-header { font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)


with st.sidebar:
    st.header("⚙️ Agent Configuration")
    st.markdown("---")
    st.info("Web Testing Agent")
    
    st.subheader("📊 Session Metrics")
    st.metric("Total Steps Captured", len(st.session_state.report_history))
    
    if st.button("🗑️ Reset Agent Session"):
        st.session_state.report_history = []
        st.session_state.last_run_time = None
        st.rerun()

    st.markdown("---")
    st.markdown("### 🛠️ Core Modules ")
    st.write("✅ Instruction Parser")
    st.write("✅ Code Generation")
    st.write("✅ Execution (Playwright)")
    st.write("✅ Assertion & Reporting")


st.title("🚀 Autonomous Web Testing Agent")
st.caption("AI Developer Intern | Infosys Springboard")


col_input, col_action = st.columns([3, 1])

with col_input:
    user_instruction = st.text_area(
        "Enter Natural Language Test Case:", 
        placeholder="e.g., Navigate to google.com, type 'LangGraph' in search, and verify if 'GitHub' is visible",
        help="The agent supports compound instructions and multi-step workflows."
    )

with col_action:
    st.write("### 🎬 Actions")
    execute_btn = st.button("▶️ Execute Autonomous Test")


if execute_btn:
    if user_instruction:
        
        with st.status("🛠️ Initializing E2E Agent Workflow...", expanded=True) as status:
            st.write("🧠 Interpreting instructions and mapping DOM elements...")
            
            
            initial_state = {
                "input": user_instruction,
                "report_history": [],
                "iteration_count": 0
            }
            
            try:
               
                final_output = asyncio.run(agent.ainvoke(initial_state))
                
                
                st.session_state.report_history = final_output.get("report_history", [])
                st.session_state.last_run_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                status.update(label="✅ Test Suite Completed Successfully!", state="complete", expanded=False)
                st.balloons()
                
            except Exception as e:
                status.update(label="❌ System Execution Failure", state="error")
                st.error(f"Root Cause: {str(e)}")
    else:
        st.warning("⚠️ Input required: Please provide a test instruction to begin.")


if st.session_state.report_history:
    st.markdown("---")
    st.header("📋 Structured Test Execution Report")
    
   
    res_pass = len([s for s in st.session_state.report_history if "SUCCESS" in s['status']])
    res_fail = len(st.session_state.report_history) - res_pass
    
    met1, met2, met3 = st.columns(3)
    met1.metric("Total Steps", len(st.session_state.report_history))
    met2.metric("Passed", res_pass)
    met3.metric("Failed", res_fail, delta=f"-{res_fail}" if res_fail > 0 else 0, delta_color="inverse")

   
    for i, step in enumerate(st.session_state.report_history):
        is_passed = "SUCCESS" in step["status"]
        status_icon = "🟢" if is_passed else "🔴"
        
        with st.container():
            st.markdown(f"#### {status_icon} Step {i+1}: {step['action'].upper()}")
            with st.expander("View Runtime Details & Adaptive DOM Mapping", expanded=not is_passed):
                st.write(f"**Action Target:** `{step.get('target', 'N/A')}`")
                if is_passed:
                    st.success(f"**Execution Log:** {step['details']}")
                else:
                    st.error(f"**Error Log:** {step['details']}")
    
 
    st.markdown("---")
    final_report_json = json.dumps({
        "timestamp": st.session_state.last_run_time,
        "instruction": user_instruction,
        "steps": st.session_state.report_history
    }, indent=4)

    st.download_button(
        label="📥 Download Structured JSON Report",
        data=final_report_json,
        file_name=f"E2E_Test_Report_{datetime.now().strftime('%H%M%S')}.json",
        mime="application/json",
        help="Export the final test results for documentation."
    )