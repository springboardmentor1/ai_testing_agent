"""
AI Web Test Agent - Professional Dark Theme Edition
Enterprise-grade UI with modern design
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules
from app.agents.test_agent_enhanced import agent
from app.data.excel_data_manager import ExcelDataManager


# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AI Test Automation Platform",
    page_icon="favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================== INITIALIZE DATA MANAGER ====================
@st.cache_resource
def get_data_manager():
    return ExcelDataManager()


data_manager = get_data_manager()


# ==================== PROFESSIONAL DARK THEME CSS ====================
st.markdown("""
<style>

/* ================= GLOBAL ================= */

.stApp {
    background: #F2F2F2;
}

.main {
    background-color: transparent;
}

/* ================= HEADER ================= */

.professional-header {
    background: #EAE4D5;
    padding: 3rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid #B6B09F;
}

.professional-header h1 {
    color: #2c2c2c;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0;
}

.professional-header p {
    color: #555555;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

/* ================= CARDS ================= */

.metric-card {
    background: #FFFFFF;
    padding: 1.5rem;
    border-radius: 10px;
    border: 1px solid #EAE4D5;
    transition: all 0.3s ease;
}

.metric-card:hover {
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
    transform: translateY(-2px);
}

/* ================= BUTTONS ================= */

.stButton > button {
    width: 100%;
    background: #B6B09F;
    color: #FFFFFF;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    font-weight: 600;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(182, 176, 159, 0.4);
}

.stButton > button:hover {
    background: #9f9988;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(182, 176, 159, 0.5);
}

.stButton > button:active {
    transform: scale(0.98);
}

/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: #EAE4D5;
    border-right: 1px solid #B6B09F;
}

section[data-testid="stSidebar"] * {
    color: #2c2c2c !important;
}

/* ================= INPUT FIELDS ================= */

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background-color: #FFFFFF;
    border: 1px solid #B6B09F;
    color: #2c2c2c;
    border-radius: 8px;
    padding: 0.6rem;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #B6B09F;
    box-shadow: 0 0 0 2px rgba(182, 176, 159, 0.3);
}

/* ================= TABS ================= */

.stTabs [data-baseweb="tab-list"] {
    background-color: #EAE4D5;
    border-radius: 8px;
    padding: 0.4rem;
}

.stTabs [data-baseweb="tab"] {
    color: #666666;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background-color: #B6B09F;
    color: #FFFFFF;
    border-radius: 6px;
}

/* ================= METRICS ================= */

[data-testid="stMetricValue"] {
    color: #2c2c2c;
    font-size: 2rem;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #666666;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* ================= DATAFRAME ================= */

.stDataFrame {
    background-color: #FFFFFF;
    border-radius: 8px;
    border: 1px solid #EAE4D5;
}

/* ================= ALERT BOXES ================= */

.stAlert {
    background-color: #FFFFFF;
    border-left: 4px solid #B6B09F;
    border-radius: 8px;
}

/* ================= HEADINGS ================= */

h1, h2, h3, h4, h5, h6 {
    color: #2c2c2c !important;
    font-weight: 600;
}

/* ================= TEXT ================= */

p, span, label {
    color: #444444;
}

/* ================= LINKS ================= */

a {
    color: #7a7466;
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* ================= DIVIDER ================= */

hr {
    border-color: #EAE4D5;
    margin: 2rem 0;
}

/* ================= SCROLLBAR ================= */

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #B6B09F;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #9f9988;
}

</style>
""", unsafe_allow_html=True)



# ==================== SIDEBAR NAVIGATION ====================
st.sidebar.markdown("# AI Test Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Execute Tests", "Analytics Dashboard", "Test History", "Data Management", "Documentation"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.info("**Playwright Engine** • **LangGraph Workflow** • **Intelligent Automation**")


# ==================== PAGE 1: EXECUTE TESTS ====================
if page == "Execute Tests":
    st.markdown("""
    <div class="professional-header">
        <h1>AI Test Automation Platform</h1>
        <p>Enterprise-Grade E2E Testing with Natural Language Processing</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Actions
    st.subheader("Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Local Authentication Test", use_container_width=True):
            st.session_state.instruction = """open browser go to http://127.0.0.1:5500/login.html
                type admin into #username
                type admin123 into #password
                click #loginBtn"""
        
        if st.button("YouTube Search & Play", use_container_width=True):
            st.session_state.instruction = """open browser go to https://www.youtube.com
                search automation testing tutorial
                wait 3000
                click first video"""
    
    with col2:
        if st.button("Google Search Test", use_container_width=True):
            st.session_state.instruction = """open browser go to https://www.google.com
                search python playwright documentation"""
        
        if st.button("Amazon Product Search", use_container_width=True):
            st.session_state.instruction = """open browser go to https://www.amazon.in
                search wireless keyboard"""
    
    st.markdown("---")
    
    # Test Input
    st.subheader("Test Configuration")
    instruction = st.text_area(
        "Natural Language Test Instructions",
        value=st.session_state.get("instruction", ""),
        height=120,
        placeholder="Enter your test scenario in plain English...\nExample: open browser search for latest tech news and capture screenshot",
        help="Describe your test scenario using natural language"
    )
    
    # Execute Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        run_button = st.button("Execute Test", type="primary", use_container_width=True)
    
    # Test Execution
    if run_button and instruction:
        with st.spinner("Processing test workflow through LangGraph..."):
            try:
                # Invoke agent
                result = agent.invoke({
                    "user_instruction": instruction,
                    "parsed_steps": [],
                    "parsing_status": "",
                    "parsing_errors": "",
                    "browser_open": False,
                    "current_url": "",
                    "logged_in": False,
                    "generated_code": "",
                    "code_file_path": "",
                    "execution_status": "",
                    "execution_output": "",
                    "execution_errors": "",
                    "retry_count": 0,
                    "test_passed": False
                })
                
                # Save to database
                test_id = data_manager.save_test_result(
                    instruction=instruction,
                    state=result,
                    execution_result={
                        "status": result.get("execution_status", "unknown"),
                        "output": result.get("execution_output", ""),
                        "errors": result.get("execution_errors", ""),
                        "return_code": 0 if result.get("test_passed") else 1
                    }
                )
                
                st.success(f"Test ID: {test_id} | Execution Complete")
                
                st.markdown("---")
                
                # Status Display
                if result.get("test_passed"):
                    st.markdown("""
                    <div class="status-success">
                        <h2 style="margin:0; font-size:1.5rem;">TEST PASSED</h2>
                        <p style="margin:0.5rem 0 0 0; opacity:0.9;">All validation steps completed successfully</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="status-failure">
                        <h2 style="margin:0; font-size:1.5rem;">TEST FAILED</h2>
                        <p style="margin:0.5rem 0 0 0; opacity:0.9;">Review execution logs for error details</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # State Metrics
                st.subheader("Workflow State Tracking")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Browser Status", "Active" if result.get("browser_open") else "Closed")
                
                with col2:
                    url = result.get("current_url", "N/A")
                    st.metric("Target URL", url[:25] + "..." if len(url) > 25 else url)
                
                with col3:
                    st.metric("Auth Status", "Authenticated" if result.get("logged_in") else "Guest")
                
                with col4:
                    st.metric("Retry Count", result.get("retry_count", 0))
                
                # Detailed Results
                tab1, tab2, tab3, tab4 = st.tabs([
                    "Test Steps",
                    "Generated Code",
                    "Execution Logs",
                    "Full Report"
                ])
                
                with tab1:
                    st.json(result.get("parsed_steps", []))
                
                with tab2:
                    st.code(result.get("generated_code", ""), language="python")
                    st.caption(f"Saved to: {result.get('code_file_path', 'N/A')}")
                
                with tab3:
                    st.text_area("Output", result.get("execution_output", "No output"), height=250)
                    
                    if result.get("execution_errors"):
                        st.error("**Error Details:**")
                        st.text(result.get("execution_errors"))
                
                with tab4:
                    log_data = data_manager.get_test_by_id(test_id)
                    if log_data:
                        st.json(log_data)
                        
                        st.download_button(
                            label="Download Full Report",
                            data=str(log_data),
                            file_name=f"test_report_{test_id}.json",
                            mime="application/json"
                        )
                
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")
                import traceback
                with st.expander("Technical Details"):
                    st.code(traceback.format_exc())


# ==================== PAGE 2: ANALYTICS DASHBOARD ====================
elif page == "Analytics Dashboard":
    st.markdown("""
    <div class="professional-header">
        <h1>Analytics Dashboard</h1>
        <p>Real-time metrics and performance insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    stats = data_manager.get_statistics()
    
    # Key Metrics
    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Executions", stats['total_tests'])
    
    with col2:
        st.metric("Success Rate", f"{stats['pass_rate']:.1f}%")
    
    with col3:
        st.metric("Avg Duration", f"{stats['avg_duration']:.2f}s")
    
    with col4:
        st.metric("Total Steps", stats['total_steps'])
    
    st.markdown("---")
    
    if stats['total_tests'] > 0:
        col1, col2 = st.columns(2)
        
        # Pass/Fail Distribution
        with col1:
            st.subheader("Pass/Fail Distribution")
            fig = go.Figure(data=[go.Pie(
                labels=['Passed', 'Failed'],
                values=[stats['passed'], stats['failed']],
                marker_colors=['#059669', '#dc2626'],
                hole=0.4
            )])
            fig.update_layout(
                height=300,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Activity Metrics
        with col2:
            st.subheader("Activity Metrics")
            st.metric("Auth Checks", stats['login_checks'])
            st.metric("Screenshots", stats['screenshots'])
            st.metric("Passed", stats['passed'])
            st.metric("Failed", stats['failed'])
        
        # Timeline
        df = data_manager.get_all_tests()
        if not df.empty and 'timestamp' in df.columns:
            st.subheader("Execution Timeline")
            
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df_sorted = df.sort_values('timestamp')
            
            fig = px.scatter(
                df_sorted,
                x='timestamp',
                y='duration_seconds',
                color='passed',
                color_discrete_map={True: '#059669', False: '#dc2626'},
                title="Duration Trend Analysis"
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(30,41,59,0.6)',
                font=dict(color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("No test data available. Execute your first test to see analytics.")


# ==================== PAGE 3: TEST HISTORY ====================
elif page == "Test History":
    st.markdown("""
    <div class="professional-header">
        <h1>Test Execution History</h1>
        <p>Search and review all test executions</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input(
            "Search Tests",
            placeholder="Enter keywords to filter results..."
        )
    
    with col2:
        limit = st.selectbox("Display Count", [10, 20, 50, 100], index=0)
    
    # Fetch data
    if search_query:
        df = data_manager.search_tests(search_query)
        st.info(f"Found {len(df)} matching records")
    else:
        df = data_manager.get_recent_tests(limit)
    
    if not df.empty:
        st.dataframe(
            df[['test_id', 'timestamp', 'instruction', 'status', 'passed', 'duration_seconds', 'steps_count']],
            use_container_width=True,
            height=400
        )
        
        st.markdown("---")
        st.subheader("Detailed View")
        
        test_ids = df['test_id'].tolist()
        selected_id = st.selectbox("Select Test", test_ids)
        
        if st.button("Load Details"):
            test_data = data_manager.get_test_by_id(selected_id)
            
            if test_data:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Status", test_data['execution']['status'].upper())
                
                with col2:
                    st.metric("Duration", f"{test_data['execution']['duration_seconds']}s")
                
                with col3:
                    st.metric("Steps", test_data['metadata']['steps_count'])
                
                tab1, tab2, tab3 = st.tabs(["Steps", "Code", "Results"])
                
                with tab1:
                    st.json(test_data['parsed_steps'])
                
                with tab2:
                    st.code(test_data['generated_code'], language="python")
                
                with tab3:
                    st.text_area("Output", test_data['execution']['output'], height=200)
                    if test_data['execution']['errors']:
                        st.error("Errors:")
                        st.text(test_data['execution']['errors'])
    else:
        st.info("No test history available.")


# ==================== PAGE 4: DATA MANAGEMENT ====================
elif page == "Data Management":
    st.markdown("""
    <div class="professional-header">
        <h1>Data Management</h1>
        <p>Export and manage test data</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Excel Export")
        st.info("Complete test history in Excel format")
        
        if os.path.exists(data_manager.excel_path):
            with open(data_manager.excel_path, 'rb') as f:
                st.download_button(
                    label="Download Excel File",
                    data=f,
                    file_name="test_history.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
        else:
            st.warning("No data available")
    
    with col2:
        st.markdown("### CSV Export")
        st.info("Spreadsheet-compatible format")
        
        if st.button("Generate CSV", use_container_width=True):
            csv_path = data_manager.export_to_csv()
            with open(csv_path, 'r') as f:
                st.download_button(
                    label="Download CSV File",
                    data=f,
                    file_name="test_history.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    st.markdown("---")
    
    # Data Preview
    st.subheader("Data Preview")
    df = data_manager.get_all_tests()
    
    if not df.empty:
        st.dataframe(df.head(10), use_container_width=True)
        st.caption(f"Showing 10 of {len(df)} total records")
        
        st.markdown("### Storage Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Records", len(df))
        
        with col2:
            st.metric("File Size", f"{os.path.getsize(data_manager.excel_path) / 1024:.1f} KB")
        
        with col3:
            json_files = len([f for f in os.listdir(data_manager.logs_dir) if f.endswith('.json')])
            st.metric("JSON Logs", json_files)
    else:
        st.info("No data available for export")
    
    st.markdown("---")
    
    # Danger Zone
    with st.expander("Danger Zone", expanded=False):
        st.warning("**WARNING:** This action will permanently delete all test data")
        
        confirm = st.checkbox("I understand this cannot be undone")
        
        if confirm:
            if st.button("Clear All Data", type="primary"):
                data_manager.clear_all_data()
                st.success("All data has been cleared")
                st.rerun()


# ==================== PAGE 5: DOCUMENTATION ====================
elif page == "Documentation":
    st.markdown("""
    <div class="professional-header">
        <h1>Documentation</h1>
        <p>Complete technical reference and guides</p>
    </div>
    """, unsafe_allow_html=True)
    
    doc_section = st.radio(
        "Select Section",
        ["Overview", "Quick Start", "Test Syntax", "Workflow", "Data Model", "API Reference"],
        horizontal=True
    )
    
    if doc_section == "Overview":
        st.markdown("""
        ## Platform Overview
        
        ### Description
        Enterprise-grade automated testing platform that converts natural language 
        into executable Playwright tests using advanced LLM technology.
        
        ### Core Features
        - Natural language test authoring
        - Automated Playwright code generation
        - Intelligent DOM mapping with fallback selectors
        - Comprehensive error handling
        - Excel/CSV data persistence
        - Real-time analytics
        - Complete audit trail
        
        ### Technology Stack
        - Python 3.10+
        - Streamlit (Web Interface)
        - LangGraph (Workflow Engine)
        - Playwright (Browser Automation)
        - Groq API (LLM Provider)
        - Pandas (Data Processing)
        - Plotly (Visualization)
        
        ### Architecture
        ```
        Input → Parser → State Tracker → Code Generator → 
        Executor → Data Storage → Analytics
        ```
        """)
    
    elif doc_section == "Quick Start":
        st.markdown("""
        ## Quick Start Guide
        
        ### Setup
        
        ```bash
        # Install dependencies
        pip install -r requirements.txt
        
        # Install browsers
        playwright install chromium
        
        # Configure API
        echo GROQ_API_KEY=your_key > .env
        
        # Launch platform
        streamlit run streamlit_app.py
        ```
        
        ### First Test
        
        1. Navigate to Execute Tests
        2. Enter: `open browser search for AI testing tools`
        3. Click Execute Test
        4. Review results in Analytics Dashboard
        """)
    
    elif doc_section == "Test Syntax":
        st.markdown("""
        ## Test Syntax Reference
        
        ### Supported Operations
        
        | Operation | Syntax Example |
        |-----------|---------------|
        | Navigation | `open browser go to example.com` |
        | Search | `search for keyword` |
        | Click | `click the submit button` |
        | Input | `type text into field` |
        | Auth Check | `check if logged in` |
        | Screenshot | `capture screenshot name.png` |
        | Wait | `wait 3 seconds` |
        | Assert | `verify page contains text` |
        
        ### Best Practices
        
        - Use clear, descriptive language
        - One operation per line
        - Avoid technical selectors
        - Provide context when needed
        """)
    
    elif doc_section == "Workflow":
        st.markdown("""
        ## LangGraph Workflow
        
        ### Process Flow
        
        ```
        1. Parse (with retry)
           ↓
        2. Track State
           ↓
        3. Generate Code
           ↓
        4. Save File
           ↓
        5. Execute (with retry)
           ↓
        Complete
        ```
        
        ### State Management
        
        The workflow tracks:
        - Instruction parsing status
        - Browser state (open/closed)
        - Current URL
        - Authentication status
        - Execution results
        - Retry attempts
        """)
    
    elif doc_section == "Data Model":
        st.markdown("""
        ## Data Model
        
        ### Excel Schema
        
        - test_id: Unique identifier
        - timestamp: Execution time
        - instruction: User input
        - status: passed/failed/timeout
        - duration_seconds: Execution time
        - steps_count: Operation count
        - browser_opened: Boolean
        - url_visited: Target URL
        - errors: Error messages
        
        ### Storage Structure
        
        ```
        project/
        ├── test_history.xlsx
        ├── test_logs/*.json
        ├── screenshots/*.png
        └── app/generated_tests/*.py
        ```
        """)
    
    elif doc_section == "API Reference":
        st.markdown("""
        ## API Reference
        
        ### ExcelDataManager
        
        ```python
        from app.data.excel_data_manager import data_manager
        
        # Save result
        test_id = data_manager.save_test_result(
            instruction="test",
            state=result,
            execution_result=data
        )
        
        # Retrieve data
        df = data_manager.get_all_tests()
        stats = data_manager.get_statistics()
        
        # Export
        data_manager.export_to_csv("output.csv")
        ```
        
        ### Test Agent
        
        ```python
        from app.agents.test_agent_enhanced import agent
        
        result = agent.invoke({
            "user_instruction": "test command",
            # ... state fields
        })
        ```
        """)


# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="text-align: center; font-size: 0.8em; color: #94a3b8;">
        <p><strong>AI Test Platform</strong></p>
        <p>Version 1.0.0 | Enterprise Edition</p>
        <p>Powered by Playwright & LangGraph</p>
    </div>
""", unsafe_allow_html=True)