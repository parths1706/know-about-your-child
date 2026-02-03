import streamlit as st

def init_session():
    defaults = {
        "step": 1,
        "basic_info": {},
        "questions": [],
        "answers": {},
        "result": None,

        
        "question_page": 0,
        "questions_per_page": 4,
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
