import streamlit as st
import json
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm
from ui.style import load_css

MIN_QUESTIONS = 7

def render_dynamic_questions():
    load_css()
    info = st.session_state.basic_info

    # ---------- INIT ----------
    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    # ---------- STOP ----------
    if len(st.session_state.questions_history) >= MIN_QUESTIONS:
        st.session_state.screen = "result"
        st.rerun()

    # ---------- HISTORY ----------
    history_text = "\n".join(
        [f"Q: {q['question']}\nA: {q['answer']}"
         for q in st.session_state.questions_history]
    ) or "No previous questions yet."

    # ---------- GENERATE QUESTION (ONCE) ----------
    if st.session_state.current_question is None:
        with st.spinner("🧠 Preparing next question..."):
            prompt = next_question_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt, expect_json=True)


            if response == "__RATE_LIMIT__":
                st.warning("Daily AI limit reached. Please try later.")
                st.stop()

            try:
                st.session_state.current_question = json.loads(response)
            except:
                st.error("Failed to load next question.")
                st.stop()

    q = st.session_state.current_question
    step = len(st.session_state.questions_history) + 1

    # ---------- UI ----------
    st.markdown(
        f"<div class='progress-text'>Question {step} of {MIN_QUESTIONS}</div>",
        unsafe_allow_html=True
    )
    st.progress(step / MIN_QUESTIONS)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='question'>{q['question']}</div>",
        unsafe_allow_html=True
    )

    answer = None

    # ---------- TAP-ONLY ANSWERS ----------
    if q["type"] == "yesno":
        answer = st.radio(
            "",
            ["Yes", "No", "Sometimes"],
            horizontal=True,
            label_visibility="collapsed",
            key=f"ans_{step}"
        )

    elif q["type"] == "mcq":
        answer = st.radio(
            "",
            q["options"],
            label_visibility="collapsed",
            key=f"ans_{step}"
        )

    elif q["type"] == "range":
        scale = q.get("scale", ["Low", "Medium", "High"])
        idx = st.slider(
            "",
            0,
            len(scale) - 1,
            label_visibility="collapsed",
            key=f"ans_{step}"
        )
        answer = scale[idx]

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- NEXT ----------
    if st.button("Next →", type="primary"):
        st.session_state.questions_history.append({
            "question": q["question"],
            "answer": answer
        })
        st.session_state.current_question = None
        st.rerun()
