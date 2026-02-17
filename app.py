import streamlit as st
import asyncio
import pandas as pd
import json
import re
from playwright.async_api import async_playwright, TimeoutError
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import sys

# ===============================
# ENV + WINDOWS FIX
# ===============================
load_dotenv()

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Agent to Test Websites Automatically",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# BEAUTIFUL LIGHT ANIMATED UI
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(-45deg, #89f7fe, #66a6ff, #a18cd1, #fbc2eb);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
    color: black;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1 {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #1f1f1f;
}
label {
    font-size: 22px !important;
    font-weight: 600 !important;
}
.stTextArea textarea {
    background-color: white !important;
    color: black !important;
    border-radius: 15px;
    padding: 15px;
    font-size: 20px !important;
    border: none;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}
.stButton>button {
    background: linear-gradient(45deg, #ff512f, #dd2476);
    color: white;
    font-weight: bold;
    border-radius: 12px;
    height: 3.2em;
    width: 100%;
    font-size: 20px !important;
    border: none;
}
.stDataFrame {
    background-color: white;
    color: black;
    border-radius: 15px;
    padding: 10px;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #667eea, #764ba2);
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🤖 AI Agent to Test Websites Automatically</h1>", unsafe_allow_html=True)

# ===============================
# LLM
# ===============================
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

if "history" not in st.session_state:
    st.session_state.history = []

# ===============================
# VALIDATION
# ===============================
def validate_search(text):
    if not text or not text.strip():
        return "Empty search"
    if re.search(r"[#@$%^&*+=\[\]{}|\\]", text):
        return "Invalid characters in search"
    return None

# ===============================
# PARSE INSTRUCTION
# ===============================
def parse_instruction(user_input):
    prompt = f"""
    Convert instruction into JSON:

    {{
      "website": "",
      "search": ""
    }}

    Extract website like amazon.com
    If no search mentioned, keep search empty.
    Return ONLY JSON.

    Instruction: {user_input}
    """

    response = llm.invoke([HumanMessage(content=prompt)])

    try:
        return json.loads(response.content)
    except:
        return None

# ===============================
# EXECUTION
# ===============================
async def run_test(website, search_text):

    status = "Pass"
    steps = ""
    error_reason = ""

    async with async_playwright() as p:

        # ✅ Added slow_mo for visible automation
        browser = await p.chromium.launch(headless=False, slow_mo=300)
        page = await browser.new_page()
        page.set_default_timeout(20000)

        try:
            if not website:
                return "Fail", steps, "Website not provided"

            website = website.strip().lower()

            if "." not in website:
                website = "www." + website + ".com"
            elif not website.startswith("www"):
                website = "www." + website

            if not website.startswith("http"):
                website = "https://" + website

            steps += f"Opened {website} → "

            response = await page.goto(website, timeout=20000)

            if response is None or response.status >= 400:
                await browser.close()
                return "Fail", steps, f"HTTP Error {response.status if response else 'N/A'}"

            await page.wait_for_load_state("domcontentloaded")

            # Extra wait for YouTube dynamic load
            if "youtube.com" in website:
                await page.wait_for_selector("input[name='search_query']", timeout=15000)

        except Exception:
            await browser.close()
            return "Fail", steps, "Invalid domain or site not reachable"

        # No search case
        if not search_text or not search_text.strip():
            await asyncio.sleep(2)
            await browser.close()
            return "Pass", steps + "No search required", ""

        invalid = validate_search(search_text)
        if invalid:
            await browser.close()
            return "Fail", steps, invalid

        # ======================
        # Site-specific selectors
        # ======================
        selector = None
        wait_selector = None

        if "google.com" in website:
            selector = "input[name='q']"
            wait_selector = "#search"

        elif "youtube.com" in website:
            selector = "input[name='search_query']"
            wait_selector = "ytd-video-renderer"

        elif "amazon.com" in website:
            selector = "input#twotabsearchtextbox"
            wait_selector = "div.s-main-slot"

        elif "myntra.com" in website:
            selector = "input[placeholder='Search for products, brands and more']"
            wait_selector = "ul.results-base"

        else:
            selector = "input[name='q'], input[type='search'], input[placeholder*='Search']"
            wait_selector = "body"

        try:
            input_box = page.locator(selector).first
            await input_box.wait_for(timeout=15000)

            if await input_box.count() == 0:
                await browser.close()
                return "Fail", steps, "Search box not found"

            # ✅ Type slowly for visibility
            await input_box.click()
            await input_box.type(search_text, delay=150)
            await page.keyboard.press("Enter")

            # Wait for results
            await page.wait_for_selector(wait_selector, timeout=20000)

            steps += f"Searched '{search_text}' successfully"

            await asyncio.sleep(3)

        except TimeoutError:
            await browser.close()
            return "Fail", steps, "Search timeout"

        except Exception as e:
            await browser.close()
            return "Fail", steps, f"Search failed: {str(e)}"

        await browser.close()

    return status, steps, error_reason

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("📜 Execution History")

if st.session_state.history:
    for item in reversed(st.session_state.history):
        icon = "🟢" if item["Status"] == "Pass" else "🔴"
        st.sidebar.markdown(f"{icon} {item['Test Case']}")
else:
    st.sidebar.info("No tests executed yet.")

# ===============================
# INPUT
# ===============================
user_input = st.text_area(
    "📝 Enter Test Instruction",
    height=130,
    placeholder="Example: open youtube.com search aptitude"
)

if st.button("🚀 Execute Test"):

    parsed = parse_instruction(user_input)

    if parsed is None:
        st.error("Invalid instruction format.")
    else:
        website = parsed.get("website", "")
        search = parsed.get("search", "")

        status, steps, error_reason = asyncio.run(run_test(website, search))

        st.session_state.history.append({
            "Test Case": user_input,
            "Steps": steps,
            "Status": status,
            "Failure Reason": error_reason if status == "Fail" else "N/A"
        })

        if status == "Pass":
            st.success("✅ Test Passed")
        else:
            st.error(f"❌ Test Failed: {error_reason}")

# ===============================
# REPORT
# ===============================
if st.session_state.history:
    st.subheader("📊 Test Execution Report")

    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇ Download Report",
        df.to_csv(index=False),
        "test_report.csv",
        "text/csv"
    )
