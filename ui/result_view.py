import streamlit as st
from ai.prompts import analysis_prompt
from ai.llm_client import ask_llm

def render_result():
    info = st.session_state.basic_info

    # ---------- FORMAT HISTORY ----------
    history_text = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}"
        for item in st.session_state.questions_history
    ])

    # ---------- GENERATE RESULT ONCE ----------
    if "result" not in st.session_state:
        with st.spinner("🔍 Generating personalized insights..."):
            prompt = analysis_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt)

            if response == "__RATE_LIMIT__":
                st.warning("⚠️ Daily AI limit reached. Please try again tomorrow.")
                st.stop()

            st.session_state.result = response

    # ---------- UI ----------
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(st.session_state.result, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔁 Start Over"):
        for key in [
            "questions_history",
            "asked_domains",
            "current_question",
            "result"
        ]:
            if key in st.session_state:
                del st.session_state[key]

        st.session_state.screen = "basic"
        st.rerun()
