import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm
from utils.session import reset_flow

def render_result():
    info = st.session_state.basic_info

    # Format history for analysis
    history_text = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}\n"
        for item in st.session_state.questions_history
    ])

    if "result" not in st.session_state:
        with st.spinner("📚 Analyzing your child..."):
            response = ask_llm(
                analysis_prompt(
                    info["region"],
                    info["age"],
                    info["gender"],
                    history_text
                )
            )
            st.session_state.result = response

    with st.container():
        # Check if result has sections
        if "1️⃣" in st.session_state.result:
            result_parts = st.session_state.result.split("2️⃣")
            
            # Section 1: Insights
            st.markdown('<div class="card-header"><h3>🌱 Child Insights</h3></div>', unsafe_allow_html=True)
            st.write(result_parts[0].replace("1️⃣", "").strip())
            
            # Section 2: Tips
            if len(result_parts) > 1:
                st.markdown('<div class="card-header"><h3>💜 Parenting Tips</h3></div>', unsafe_allow_html=True)
                st.write(result_parts[1].strip())
        else:
            # Fallback if no sections
            st.markdown('<div class="card-header"><h3>🌱 Child Insights</h3></div>', unsafe_allow_html=True)
            st.write(st.session_state.result)
        
        if st.button("Start Over", type="primary"):
            reset_flow()
            st.session_state.screen = "intro"
            st.rerun()
