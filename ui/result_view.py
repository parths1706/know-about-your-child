import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm
from utils.session import reset_flow

def render_result():
    info = st.session_state.basic_info

    if not st.session_state.result:
        with st.spinner("Analyzing insights..."):
            prompt = analysis_prompt(
                info["region"],
                info["age"],
                info["gender"],
                st.session_state.answers
            )
            st.session_state.result = ask_llm(prompt)

    result = st.session_state.result.split("2️⃣")

    with st.container():
        # Section 1: Insights
        st.markdown('<div class="card-header"><h3>🌱 Child Insights</h3></div>', unsafe_allow_html=True)
        st.write(result[0].replace("1️⃣", "").strip())
        
        # Section 2: Tips
        if len(result) > 1:
            st.markdown('<div class="card-header"><h3>💜 Parenting Tips</h3></div>', unsafe_allow_html=True)
            st.write(result[1].strip())
        
        if st.button("Start Over", type="primary"):
            reset_flow()
            st.session_state.screen = "intro"
            st.rerun()
