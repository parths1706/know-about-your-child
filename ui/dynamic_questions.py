import streamlit as st
import json
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm

MIN_QUESTIONS = 7

ALLOWED_DOMAINS = {
    "belief_system",
    "discipline_style",
    "emotional_response",
    "respect_elders",
    "independence",
    "parent_involvement",
    "adaptability"
}

def render_dynamic_questions():
    info = st.session_state.basic_info

    # ---------- STATE INIT ----------
    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    if "asked_domains" not in st.session_state:
        st.session_state.asked_domains = set()

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    # ---------- STOP CONDITION ----------
    if len(st.session_state.questions_history) >= MIN_QUESTIONS:
        st.session_state.screen = "result"
        st.rerun()

    # ---------- FORMAT HISTORY ----------
    history_text = "\n".join([
        f"Q ({item['domain']}): {item['question']}\nA: {item['answer']}"
        for item in st.session_state.questions_history
    ]) if st.session_state.questions_history else "No previous questions yet."

    # ---------- GENERATE QUESTION (ONCE PER STEP) ----------
    if st.session_state.current_question is None:
        with st.spinner("🧠 Thinking about the next question..."):
            prompt = next_question_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt)

            if response == "__RATE_LIMIT__":
                st.warning("⚠️ Daily AI limit reached. Please try again later.")
                st.stop()

            try:
                q = json.loads(response)
            except:
                st.error("Failed to generate question. Please refresh.")
                st.stop()

            # ---------- HARD VALIDATION ----------
            if (
                q.get("domain") not in ALLOWED_DOMAINS or
                q.get("domain") in st.session_state.asked_domains or
                q.get("type") not in ["yesno", "mcq", "range"]
            ):
                st.session_state.current_question = None
                st.rerun()

            st.session_state.current_question = q
    else:
        q = st.session_state.current_question

    # ---------- UI ----------
    step = len(st.session_state.questions_history) + 1

    st.markdown(
        f"<div class='progress-text'>Question {step} of {MIN_QUESTIONS}</div>",
        unsafe_allow_html=True
    )
    st.progress(step / MIN_QUESTIONS)

    st.markdown(
        f"<div class='question'>{q['question']}</div>",
        unsafe_allow_html=True
    )

    answer = None

    # ---------- ANSWER TYPES ----------
    if q["type"] == "yesno":
        answer = st.radio(
            "hidden",
            ["Yes", "No", "Sometimes"],
            horizontal=True,
            label_visibility="collapsed",
            key=f"ans_{step}"
        )

    elif q["type"] == "mcq":
        answer = st.radio(
            "hidden",
            q["options"],
            label_visibility="collapsed",
            key=f"ans_{step}"
        )

    elif q["type"] == "range":
        scale = q.get("scale", ["Low", "Medium", "High"])
        idx = st.slider(
            "hidden",
            0,
            len(scale) - 1,
            label_visibility="collapsed",
            key=f"ans_{step}"
        )
        answer = scale[idx]

    # ---------- NEXT ----------
    if st.button("Next →", type="primary"):
        st.session_state.questions_history.append({
            "domain": q["domain"],
            "question": q["question"],
            "answer": answer
        })

        st.session_state.asked_domains.add(q["domain"])
        st.session_state.current_question = None
        st.rerun()
