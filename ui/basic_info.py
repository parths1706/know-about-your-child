import streamlit as st

from utils.session import reset_flow


def render_basic_info():
    with st.container():
        # Section title
        st.markdown("<h3 class='section-title'>Let's get started! 🎈</h3>", unsafe_allow_html=True)

        # -------- REGION --------
        current_region = st.session_state.basic_info.get("region", "India")
        regions = ["India", "USA", "Europe", "Other"]
        
        # Ensure the detected region is in the list or add it
        if current_region not in regions:
            regions.insert(0, current_region)
            
        region = st.selectbox(
            "Where are you from?",
            regions,
            index=regions.index(current_region),
            help="Automatically detected from your IP 🌍"
        )
        
        # -------- GENDER --------
        gender = st.radio(
            "Gender",
            ["👦 Male", "👧 Female", "🧸 Other"],
            horizontal=True
        )
        
        # -------- AGE --------
        age = st.slider(
            "How old is your child?",
            min_value=0,
            max_value=15,
            value=5
        )

        # Friendly age stage indicator
        if age <= 3:
            st.markdown("<p style='text-align:center; color:#6366f1; font-weight:600;'>👶 Baby stage</p>", unsafe_allow_html=True)
        elif age <= 9:
            st.markdown("<p style='text-align:center; color:#6366f1; font-weight:600;'>🧒 Child stage</p>", unsafe_allow_html=True)
        else:
            st.markdown("<p style='text-align:center; color:#6366f1; font-weight:600;'>🧑 Teen stage</p>", unsafe_allow_html=True)

        # Continue button
        if st.button("Continue", type="primary"):
            st.session_state.basic_info = {
                "region": region,
                "age": age,
                "gender": gender.replace("👦 ", "").replace("👧 ", "").replace("🧸 ", "")
            }

            reset_flow()                          # 🔥 reset before AI
            st.session_state.screen = "transition"
            st.rerun()
