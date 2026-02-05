import streamlit as st
import json
from ai.llm_client import ask_llm
from ai.prompts import next_question_prompt

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

def init_question_state():
    if "asked_domains" not in st.session_state:
        st.session_state.asked_domains = set()

    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    if "question_count" not in st.session_state:
        st.session_state.question_count = 0

    if "current_question" not in st.session_state:
        st.session_state.current_question = None


def render_dynamic_questions():
    init_question_state()

    # If no active question, generate one
    if st.session_state.current_question is None:
        generate_next_question()

    q = st.session_state.current_question

    st.markdown(f"### Question {st.session_state.question_count + 1}")

    st.markdown(q["question"])

    answer = None

    if q["type"] == "yesno":
        answer = st.radio(
            "Select one:",
            ["Yes", "No"],
            horizontal=True,
            key=f"ans_{st.session_state.question_count}"
        )

    elif q["type"] == "mcq":
        answer = st.radio(
            "Select one:",
            q["options"],
            key=f"ans_{st.session_state.question_count}"
        )

    elif q["type"] == "range":
        answer = st.slider(
            "Select:",
            0,
            len(q["scale"]) - 1,
            format="",
            key=f"ans_{st.session_state.question_count}"
        )
        answer = q["scale"][answer]

    if st.button("Next →", type="primary"):
        save_answer(answer)


def save_answer(answer):
    q = st.session_state.current_question

    st.session_state.qa_history.append({
        "domain": q["domain"],
        "question": q["question"],
        "answer": answer
    })

    st.session_state.asked_domains.add(q["domain"])
    st.session_state.question_count += 1
    st.session_state.current_question = None

    # Enforce minimum questions
    if st.session_state.question_count >= MIN_QUESTIONS:
        if len(st.session_state.asked_domains) >= len(ALL_DOMAINS):
            st.session_state.screen = "result"
            st.rerun()

    st.rerun()


def generate_next_question():
    region = st.session_state.basic_info["region"]
    age = st.session_state.basic_info["age"]
    gender = st.session_state.basic_info["gender"]

    used = st.session_state.asked_domains
    remaining_domains = list(ALL_DOMAINS - used)

    history_text = ""
    for h in st.session_state.qa_history:
        history_text += f"{h['question']} → {h['answer']}\n"

    prompt = next_question_prompt(region, age, gender, history_text)

    raw = ask_llm(prompt)

    try:
        data = json.loads(raw)
    except Exception:
        return  # silently fail and regenerate next run

    # HARD GUARDS
    if data.get("domain") in used:
        return

    if data.get("type") not in ["yesno", "mcq", "range"]:
        return

    st.session_state.current_question = data
