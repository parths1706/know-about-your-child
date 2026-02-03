import streamlit as st
from utils.session import init_session
from ui.basic_info import render_basic_info
from ui.dynamic_questions import render_dynamic_questions
from ui.result_view import render_result

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(
    page_title="Know About Your Child",
    page_icon="💜",
    layout="centered",
    initial_sidebar_state="collapsed"
)

load_css()
init_session()

# Simple and clean header
st.markdown("""
<div class="app-header">
    <h1>💜 Know About Your Child</h1>
    <p>Personalized insights to understand and support your child better</p>
</div>
""", unsafe_allow_html=True)


if st.session_state.step == 1:
    render_basic_info()
elif st.session_state.step == 2:
    render_dynamic_questions()
elif st.session_state.step == 3:
    render_result()
