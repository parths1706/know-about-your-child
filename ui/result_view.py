import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm
from utils.session import reset_flow

def render_result():
    info = st.session_state.basic_info

    history_text = "\n".join(
        [f"Q: {q['question']}\nA: {q['answer']}"
         for q in st.session_state.questions_history]
    )

    # ---------- GENERATE RESULT ----------
    if not st.session_state.result:
        with st.spinner("🔍 Analyzing your child..."):
            prompt = analysis_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt)

            if response == "__RATE_LIMIT__":
                st.warning("Daily AI limit reached. Try later.")
                st.stop()

            st.session_state.result = response

    # ---------- UI ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(st.session_state.result, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔁 Start Over"):
        reset_flow()
        st.session_state.screen = "basic"
        st.rerun()
