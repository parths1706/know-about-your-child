import streamlit as st
import json
import urllib.request

def get_country_by_ip():
    try:
        url = "http://ip-api.com/json"
        with urllib.request.urlopen(url, timeout=3) as response:
            data = json.loads(response.read().decode())
            return data.get("country", "India")
    except:
        return "India"

def init_session():
    defaults = {
        "screen": "intro",      # intro → basic → transition → question → result
        "basic_info": {
            "region": get_country_by_ip()
        },
        "questions": [],
        "answers": {},
        "question_index": 0,
        "result": None          # ✅ ADD THIS
    }

    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def reset_flow():
    st.session_state.questions = []
    st.session_state.answers = {}
    st.session_state.question_index = 0
    st.session_state.result = None
