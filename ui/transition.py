import streamlit as st
import time
import json
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm

def render_transition():
    st.markdown("""
    <div class="transition-wrapper">
        <div class="transition-card">
            <div class="loader"></div>
            <h3>Preparing personalized questions…</h3>
            <p>Our AI is analyzing your child's profile 💜</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize questions_history if first time
    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    time.sleep(1.5)
    st.session_state.screen = "question"
    st.rerun()
