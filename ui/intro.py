import streamlit as st
from utils.session import reset_flow

def render_intro():
    with st.container():
        st.markdown("<div style='text-align:center; font-size:4rem;'>👋</div>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#4c1d95; margin-bottom:1rem;'>Welcome!</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#6b7280; font-size:1.2rem; margin-bottom:2.5rem;'>Discover personalized AI insights to help your child thrive. It only takes a minute!</p>", unsafe_allow_html=True)

        if st.button("Start My Journey ✨", type="primary"):
            reset_flow()                     # 🔥 IMPORTANT
            st.session_state.screen = "basic"
            st.rerun()
