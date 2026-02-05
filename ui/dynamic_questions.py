import streamlit as st
import json
from ai.prompts import next_question_prompt
from ai.llm_client import ask_llm

def render_dynamic_questions():
    info = st.session_state.basic_info

    if "questions_history" not in st.session_state:
        st.session_state.questions_history = []

    # Format history for prompt
    history_text = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}\n"
        for item in st.session_state.questions_history
    ]) if st.session_state.questions_history else "No previous questions yet."

    with st.container():
        # Ask AI for next question
        try:
            with st.spinner("🧠 Thinking about the next question..."):
                prompt = next_question_prompt(
                    info["region"],
                    info["age"],
                    info["gender"],
                    history_text
                )
                
                response = ask_llm(prompt)
                
                # Clean response if it contains markdown code blocks
                if "```json" in response:
                    response = response.split("```json")[1].split("```")[0].strip()
                elif "```" in response:
                    response = response.split("```")[1].split("```")[0].strip()
                
                q = json.loads(response)
                
                # Validate required fields
                if "question" not in q or "type" not in q:
                    raise ValueError("Missing required fields in response")
                    
        except Exception as e:
            st.error("Failed to generate question. Please try again.")
            st.caption(f"Debug: {str(e)[:200]}")
            if st.button("Go Back"):
                st.session_state.screen = "basic"
                st.rerun()
            return

        # Progress
        st.markdown(
            f"<div class='progress-text'>Step {len(st.session_state.questions_history)+1} of 6</div>",
            unsafe_allow_html=True
        )
        st.progress((len(st.session_state.questions_history)+1) / 6)

        # Question
        st.markdown(f"<div class='question'>{q['question']}</div>", unsafe_allow_html=True)

        answer = None

        if q["type"] == "yesno":
            answer = st.radio(
                "hidden_label",
                ["Yes", "No"],
                horizontal=True,
                label_visibility="collapsed",
                key=f"q_{len(st.session_state.questions_history)}"
            )

        elif q["type"] == "mcq":
            answer = st.radio(
                "hidden_label",
                q["options"],
                label_visibility="collapsed",
                key=f"q_{len(st.session_state.questions_history)}"
            )

        else:
            answer = st.text_area(
                "hidden_label",
                placeholder="Type briefly…",
                label_visibility="collapsed",
                height=120,
                key=f"q_{len(st.session_state.questions_history)}"
            )

        if st.button("Next →", type="primary"):
            st.session_state.questions_history.append({
                "question": q["question"],
                "type": q["type"],
                "answer": answer
            })

            # Stop after enough info
            if len(st.session_state.questions_history) >= 6:
                st.session_state.screen = "result"
            
            st.rerun()
