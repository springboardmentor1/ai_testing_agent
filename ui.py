import sys
import asyncio

# REQUIRED for Playwright on Windows
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from app.agents.baseline_agent import agent

st.set_page_config(page_title="AI Web Testing Agent", layout="wide")

# --- Custom CSS Styling ---
st.markdown("""
    <style>
    /* Centered Title */
    .main-title {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        color: #87CEFA;
        margin-bottom: 20px;
        animation: fadeIn 2s ease-in-out;
    }
            
   .custom-label {
        font-size: 1.5em;       /* Increase size */
        font-weight: bold;
        color: #FFEFD5;         /* Matches your title color */
        text-align: start;
        margin: 0;              /* Remove default margins */
        padding: 0;             /* Remove default padding */
        line-height: 1.2;
    }

    /* Input box styling */
    textarea {
        border: 2px solid #3498db !important;
        border-radius: 10px !important;
        font-size: 1.5em !important;
        padding: 12px !important;
        # background-color: #f9f9f9 !important;
    }
            
     /* Style for Run Test button */
    div.stButton > button:first-child {
        width: 100px;                  /* Make it wide */
        height: 30px;    
        background: linear-gradient(90deg, #4facfe, #00f2fe); 
        color: black !important;      /* Text color */
        font-size: 1.2em;             /* Slightly larger text */
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 0;
        transition: all 0.4s ease-in-out;
    }

    /* Hover effect */
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #3a7bd5, #3a6073); /* Reverse gradient */
        transform: scale(1.05);       /* Slight zoom */
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2); /* Glow effect */
    }
            
    .stColumn > div {
        display: flex;
        justify-content: center;
        align-items: center;
    }        

    /* Download button styling */
    .stDownloadButton button {
        background: linear-gradient(90deg, #3498db, #2ecc71);
        color: white !important;
        font-weight: bold;
        border-radius: 8px !important;
        
        transition: transform 0.2s ease-in-out;
    }
    .stDownloadButton button:hover {
        transform: scale(1.05);
        background: linear-gradient(90deg, #2ecc71, #3498db);
    }

    .summary-container h3 {
        text-align: center;
        font-size: 1.8em;
        font-weight: bold;
        background: linear-gradient(90deg, #4facfe, #00f2fe);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 15px;
        animation: fadeIn 1.5s ease-in-out;
    } 
            
    /* Animation keyframes */
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

# --- Title ---
st.markdown('<div class="main-title"> AI Agent for Automated Website Testing</div>', unsafe_allow_html=True)

# --- Instruction placeholder inside input box ---
placeholder_text = """- "Open YouTube and search for n8n automation"
- "Go to index.html and login with username and password"
- "Navigate to Flipkart and search for iPhone 15"

"""

st.markdown('<div class="custom-label">Enter your test instruction:</div>', unsafe_allow_html=True)
instruction = st.text_area("Test Instruction", height=200, placeholder=placeholder_text, label_visibility="hidden")

if st.button("Run"):
    if instruction.strip() == "":
        st.warning("Please enter a test instruction.")
    else:
        with st.spinner("Running your test..."):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                agent.ainvoke({"input": instruction})
            )
            loop.close()

        # --- Top row: Test completed + Pass/Fail + Download ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.success("Test completed.")

        with col2:
            # Report download
            # Extract report path from output
             output_text = result.get("output", "")
             report_line = [
                 line for line in output_text.split("\n")
                 if "HTML Report Generated" in line
             ]
    
             if report_line:
                html_path = report_line[0].split(": ", 1)[1]
                with open(html_path, "rb") as f:
                    st.download_button(
                        label="Download Test Report",
                        data=f,
                        file_name=html_path.split("\\")[-1],
                        mime="text/html"
                    )
             else:
                    st.warning("No report generated.")
            
        with col3:
            final_status = result.get("status")
        
            if final_status == "passed":
                st.success("✔️ Passed")
            elif final_status == "failed":
                st.error("❌ Failed")
            else:
                st.warning("⚠️ Unknown Status")
        
       
        # # --- Step Summary ---
        step_results = result.get("step_results", [])
        total_steps = len(step_results)
        passed_steps = sum(1 for s in step_results if s["status"] == "pass")
        failed_steps = sum(1 for s in step_results if s["status"] == "fail")
        
        st.markdown('<div class="summary-container">', unsafe_allow_html=True)
        st.subheader("📊 Test Summary")
        
        if total_steps == 0:
            st.warning("⚠️ No steps were parsed from your instruction. Please check the input format.")
        else:
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"<p style='color:#2c3e50;font-weight:bold;'>Total Steps: {total_steps}</p>", unsafe_allow_html=True)
            col2.markdown(f"<p style='color:#27ae60;font-weight:bold;'>Passed: {passed_steps}</p>", unsafe_allow_html=True)
            col3.markdown(f"<p style='color:#e74c3c;font-weight:bold;'>Failed: {failed_steps}</p>", unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)


        # --- Parsed steps ---
        st.subheader("🧩 Parsed Steps")
        for step in result.get("parsed_command", []):
            st.json(step)

        # --- Execution logs ---
        st.subheader("📄 Execution Output")
        st.code(result.get("output", ""), language="text")





