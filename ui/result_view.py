import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm
from utils.session import reset_flow

def render_result():
    info = st.session_state.basic_info

    if "result" not in st.session_state:
        with st.spinner("Analyzing your child..."):
            st.session_state.result = ask_llm(
                analysis_prompt(
                    info["region"],
                    info["age"],
                    info["gender"],
                    st.session_state.questions_history
                )
            )

    st.markdown("## 🌱 Child Insights")
    st.write(st.session_state.result)

    if st.button("Start Over"):
        reset_flow()
        st.session_state.screen = "intro"
        st.rerun()
