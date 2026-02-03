import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm

def render_result():
    info = st.session_state.basic_info

    if not st.session_state.result:
        prompt = analysis_prompt(
            info["region"],
            info["age"],
            info["gender"],
            st.session_state.answers
        )
        st.session_state.result = ask_llm(prompt)

    result = st.session_state.result.split("2️⃣")

    # Section 1: Insights
    with st.container():
        st.markdown('<div class="card-header"><h3>🌱 Child Insights</h3></div>', unsafe_allow_html=True)
        st.write(result[0].replace("1️⃣", "").strip())
    
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    # Section 2: Tips
    if len(result) > 1:
        with st.container():
            st.markdown('<div class="card-header"><h3>💜 Parenting Tips</h3></div>', unsafe_allow_html=True)
            st.write(result[1].strip())
    
    st.markdown("<div style='margin-bottom: 2rem;'></div>", unsafe_allow_html=True)

    if st.button("Start Over", type="primary"):
        st.session_state.step = 1
        st.session_state.questions = []
        st.session_state.answers = {}
        st.session_state.result = None
        st.rerun()
