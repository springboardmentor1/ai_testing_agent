import streamlit as st

def login():
    st.sidebar.title("🔐 Login")

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if username == "nehasomawanshi" and password == "1234":
        return True
    else:
        if username or password:
            st.sidebar.error("Invalid credentials")
        return False
