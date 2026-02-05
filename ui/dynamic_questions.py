import streamlit as st
import json
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm

MIN_QUESTIONS = 7

ALL_DOMAINS = {
    "belief_system",
    "discipline_style",
    "emotional_response",
    "parent_child_bond",
    "respect_elders",
    "independence",
    "adaptability"
}

def render_dynamic_questions():
    info = st.session_state.basic_info

    # ---------- STATE INIT ----------
    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    if "asked_domains" not in st.session_state:
        st.session_state.asked_domains = set()

    # ---------- STOP CONDITION ----------
    if len(st.session_state.questions_history) >= MIN_QUESTIONS:
        st.session_state.screen = "result"
        st.rerun()

    # ---------- FORMAT HISTORY ----------
    history_text = "\n".join([
        f"Q ({item['domain']}): {item['question']}\nA: {item['answer']}"
        for item in st.session_state.questions_history
    ]) if st.session_state.questions_history else "No previous questions yet."

    # ---------- ASK AI ----------
    with st.container():
        with st.spinner("🧠 Thinking about the next question..."):
            prompt = next_question_prompt(
                info["region"],
                info["age"],
                info["gender"],
                history_text
            )

            response = ask_llm(prompt)

            # Clean markdown if AI adds it
            if "```" in response:
                response = response.split("```")[1]

            try:
                q = json.loads(response)
            except:
                st.error("Something went wrong. Please refresh.")
                return

        # ---------- HARD GUARDS ----------
        if q.get("domain") in st.session_state.asked_domains:
            st.rerun()

        if q.get("type") not in ["yesno", "mcq", "range"]:
            st.rerun()

        # ---------- PROGRESS ----------
        step = len(st.session_state.questions_history) + 1
        st.markdown(
            f"<div class='progress-text'>Step {step} of {MIN_QUESTIONS}</div>",
            unsafe_allow_html=True
        )
        st.progress(step / MIN_QUESTIONS)

        # ---------- QUESTION ----------
        st.markdown(
            f"<div class='question'>{q['question']}</div>",
            unsafe_allow_html=True
        )

        answer = None

        # ---------- ANSWER TYPES (NO TEXT EVER) ----------
        if q["type"] == "yesno":
            answer = st.radio(
                "hidden_label",
                ["Yes", "No", "Sometimes"],
                horizontal=True,
                label_visibility="collapsed",
                key=f"q_{step}"
            )

        elif q["type"] == "mcq":
            answer = st.radio(
                "hidden_label",
                q["options"],
                label_visibility="collapsed",
                key=f"q_{step}"
            )

        elif q["type"] == "range":
            labels = q.get("scale", ["Low", "Medium", "High"])
            idx = st.slider(
                "hidden_label",
                0,
                len(labels) - 1,
                label_visibility="collapsed",
                key=f"q_{step}"
            )
            answer = labels[idx]

        # ---------- NEXT ----------
        if st.button("Next →", type="primary"):
            st.session_state.questions_history.append({
                "domain": q["domain"],
                "question": q["question"],
                "answer": answer
            })

            st.session_state.asked_domains.add(q["domain"])
            
            st.rerun()
