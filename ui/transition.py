import streamlit as st
import time
import json
from ai.prompts import question_prompt
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

    if not st.session_state.questions:
        try:
            info = st.session_state.basic_info
            prompt = question_prompt(info["region"], info["age"], info["gender"])
            response = ask_llm(prompt)
            
            # Clean response if it contains markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            questions = json.loads(response)
            st.session_state.questions = questions
            st.session_state.question_index = 0
        except Exception as e:
            st.error(f"Error generating questions: {e}")
            time.sleep(3)
            st.session_state.screen = "basic"
            st.rerun()

    time.sleep(1.5)
    st.session_state.screen = "question"
    st.rerun()
