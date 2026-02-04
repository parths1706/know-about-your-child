import streamlit as st
from utils.session import init_session

from ui.intro import render_intro
from ui.basic_info import render_basic_info
from ui.transition import render_transition
from ui.dynamic_questions import render_dynamic_questions
from ui.result_view import render_result


def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.set_page_config(
    page_title="Know About Your Child",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

load_css()
init_session()

# App header (navigation feel)
st.markdown("""
<div class="app-header">
    <h1>Know About Your Child</h1>
    <p>Personalized insights for your child's growth 💜</p>
</div>
""", unsafe_allow_html=True)


# -------- ROUTING --------
if st.session_state.screen == "intro":
    render_intro()

elif st.session_state.screen == "basic":
    render_basic_info()

elif st.session_state.screen == "transition":
    render_transition()

elif st.session_state.screen == "question":
    render_dynamic_questions()

elif st.session_state.screen == "result":
    render_result()
