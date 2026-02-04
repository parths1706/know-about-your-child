import streamlit as st
import json
from ai.prompts import question_prompt
from ai.llm_client import ask_llm


def render_dynamic_questions():
    questions = st.session_state.questions
    index = st.session_state.question_index
    
    if not questions:
        st.session_state.screen = "transition"
        st.rerun()
        return

    total = len(questions)

    if index >= total:
        st.session_state.screen = "result"
        st.rerun()
        return

    q = questions[index]

    with st.container():
        # Progress
        st.markdown(
            f"<div class='progress-text'>Question {index + 1} of {total}</div>",
            unsafe_allow_html=True
        )
        st.progress((index + 1) / total)

        # Question
        st.markdown(
            f"<div class='question'>{q['question']}</div>",
            unsafe_allow_html=True
        )

        key = f"q_{index}"

        # ---------- INPUT TYPES ----------
        if q["type"] == "yes_no":
            answer = st.radio(
                "hidden_label",
                ["Yes", "No"],
                key=key,
                horizontal=True,
                label_visibility="collapsed"
            )

        elif q["type"] == "options":
            answer = st.radio(
                "hidden_label",
                q["options"],
                key=key,
                label_visibility="collapsed"
            )

        elif q["type"] == "scale":
            answer = st.slider(
                "",
                1, 5, 3,
                help="1 = Very Low, 5 = Very High",
                key=key
            )

        else:
            answer = st.text_area(
                "",
                placeholder="Type your answer…",
                key=key,
                height=120
            )

        st.session_state.answers[q["question"]] = answer

        # ---------- NAV ----------
        if st.button("Next →", type="primary"):
            st.session_state.question_index += 1
            st.session_state.screen = "transition"
            st.rerun()
