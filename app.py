import asyncio
import sys


if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from agents.baseline_agent import agent


st.set_page_config(page_title="AI Web Testing Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Autonomous Web Testing Agent")
st.markdown("""
This agent interprets natural language, executes browser tests using Playwright, 
and generates a structured execution report with self-healing capabilities.
""")

with st.sidebar:
    st.header("Settings")
    st.info("Milestone 4: Reporting & UI Phase")
    if st.button("Clear History"):
        st.session_state.report_history = []
        st.rerun()


user_input = st.text_input("Enter your test instruction:", placeholder="e.g., Navigate to google.com and search for LangGraph")

if st.button("Run Test Case"):
    if user_input:
        with st.spinner(" Agent is thinking and executing..."):
          
            initial_state = {
                "input": user_input,
                "report_history": [],
                "iteration_count": 0
            }
            
            try:

                final_state = asyncio.run(agent.ainvoke(initial_state))
                
 
                st.subheader(" Structured Test Report")
                
  
                history = final_state.get("report_history", [])
                
                if not history:
                    st.info("No execution steps were recorded.")
                
                for entry in history:
                    status = entry["status"]

                    with st.expander(f"{status} | Action: {entry['action'].upper()}", expanded=True):
                        st.write(f"**Target:** {entry.get('target', 'N/A')}")
                        st.write(f"**Details:** {entry['details']}")
                        
                st.success("Test Execution Workflow Completed.")
                
            except Exception as e:
                st.error(f"An error occurred during execution: {str(e)}")
    else:
        st.warning("Please enter an instruction first.")