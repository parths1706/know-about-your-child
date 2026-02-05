import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm
from utils.session import reset_flow
from ui.style import load_css
import json

def render_result():
    # ✅ LOAD CSS FIRST
    load_css()

    info = st.session_state.basic_info

    # ✅ USE CORRECT STATE KEY
    history_text = "\n".join(
        [
            f"Q: {q['question']}\nA: {q['answer']}"
            for q in st.session_state.questions
        ]
    )

    # ---------- GENERATE RESULT ----------
    if not st.session_state.result:
        with st.spinner("🔍 Understanding your child..."):
            prompt = analysis_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt, expect_json=False)

            if response in ("__ERROR__", None):
                st.error("AI is busy. Please try again in a moment.")
                st.stop()

            st.session_state.result = response

    # ---------- UI (LET CSS HANDLE CARD) ----------
    with st.container():
        st.markdown(
            "<div class='section-title'>Know About Your Child</div>",
            unsafe_allow_html=True
        )

        st.markdown(st.session_state.result, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("🔁 Start Over", type="primary"):
            reset_flow()
            st.session_state.screen = "basic"
            st.rerun()
