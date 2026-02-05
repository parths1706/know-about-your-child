import streamlit as st
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm

def render_dynamic_questions():
    info = st.session_state.basic_info

    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    # Ask AI for next question
    prompt = next_question_prompt(
        info["region"],
        info["age"],
        info["gender"],
        st.session_state.questions_history
    )

    with st.spinner("Thinking about the next question..."):
        q = ask_llm(prompt)

    st.markdown(
        f"<div class='progress'>Question {len(st.session_state.questions_history)+1}</div>",
        unsafe_allow_html=True
    )

    st.markdown(f"<div class='question'>{q['question']}</div>", unsafe_allow_html=True)

    answer = None

    if q["type"] == "yesno":
        answer = st.radio("", ["Yes", "No"], horizontal=True)

    elif q["type"] == "mcq":
        answer = st.radio("", q["options"])

    else:
        answer = st.text_area("", placeholder="Type briefly...")

    if st.button("Next →", type="primary"):
        st.session_state.questions_history.append({
            "question": q["question"],
            "type": q["type"],
            "answer": answer
        })

        # Stop after enough info
        if len(st.session_state.questions_history) >= 6:
            st.session_state.screen = "result"
        else:
            st.rerun()
