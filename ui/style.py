import streamlit as st

def load_css():
    if "css_loaded" in st.session_state:
        return

    with open("assets/style.css", "r") as f:
        css = f.read()

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.session_state.css_loaded = True
