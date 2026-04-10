import streamlit as st

st.set_page_config(page_title="AI Test Automation Dashboard", layout="wide")

st.markdown(
    """
<style>
/* Purple gradient background */
.stApp {
  background: linear-gradient(135deg, #4c1d95 0%, #7c3aed 45%, #ec4899 100%);
}

/* Optional: make main content readable */
section[data-testid="stMain"] .block-container {
  background: rgba(255, 255, 255, 0.88);
  backdrop-filter: blur(6px);
  border-radius: 16px;
  padding: 24px;
  margin-top: 24px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.18);
}
</style>
""",
    unsafe_allow_html=True,
)

st.title("AI Test Automation Dashboard")
st.write("Purple gradient background is enabled.")

