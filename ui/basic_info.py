import streamlit as st

def render_basic_info():
    with st.container():
        # This header marker allows the CSS to target the container and style it as a card
        st.markdown('<div class="card-header"><h3>👶 Child Information</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            region = st.selectbox("Region", ["India", "USA", "Europe", "Other"], help="Select your child's region")
            gender = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)

        with col2:
            age = st.slider("Age of Child", 1, 18, 5, help="Select your child's current age")

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    if st.button("Continue →", type="primary"):
        st.session_state.basic_info = {
            "region": region,
            "age": age,
            "gender": gender
        }
        st.session_state.step = 2
        st.rerun()
