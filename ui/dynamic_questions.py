import streamlit as st
from ai.prompts import question_prompt
from ai.llm_client import ask_llm

def render_dynamic_questions():
    info = st.session_state.basic_info

    # Initialize pagination state
    if "question_page" not in st.session_state:
        st.session_state.question_page = 0

    if "questions_per_page" not in st.session_state:
        st.session_state.questions_per_page = 4

    # Generate questions only once
    if not st.session_state.questions:
        prompt = question_prompt(
            info["region"], info["age"], info["gender"]
        )
        raw = ask_llm(prompt)
        st.session_state.questions = [
            q.strip("- ").strip()
            for q in raw.split("\n")
            if q.strip()
        ]

    start = st.session_state.question_page * st.session_state.questions_per_page
    end = start + st.session_state.questions_per_page
    current_questions = st.session_state.questions[start:end]

    # --------- TITLE ---------
    st.markdown('<div class="section-title">🧠 Help Us Understand Your Child</div>', unsafe_allow_html=True)

    # --------- QUESTIONS ---------
    for i, q in enumerate(current_questions):
        with st.container():
            # Marker for card styling
            st.markdown(f'<div class="card-header"><h3>Question {start + i + 1}</h3></div>', unsafe_allow_html=True)
            st.markdown(f"<div class='question'>{q}</div>", unsafe_allow_html=True)

            st.session_state.answers[q] = st.text_area(
                label="Your Answer",
                value=st.session_state.answers.get(q, ""),
                placeholder="Type your insights here...",
                height=150,
                key=f"answer_{q}",
                label_visibility="collapsed"
            )
        st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)

    # --------- NAVIGATION BUTTONS ---------
    col1, col2 = st.columns(2)


    with col1:
        if st.session_state.question_page > 0:
            if st.button("← Back"):
                st.session_state.question_page -= 1
                st.rerun()

    with col2:
        if end < len(st.session_state.questions):
            if st.button("Next →", type="primary"):
                st.session_state.question_page += 1
                st.rerun()
        else:
            if st.button("Analyze My Child", type="primary"):
                st.session_state.step = 3
                st.rerun()
