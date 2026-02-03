def apply_theme():
    import streamlit as st

    st.markdown("""
    <style>

    /* Page background */
    .stApp {
        background-color: #f6f7fb;
        font-family: 'Inter', sans-serif;
    }

    /* Header */
    .app-header {
        font-size: 32px;
        font-weight: 700;
        color: #4b2aad;
        margin-bottom: 10px;
    }

    .app-subtitle {
        color: #6b7280;
        margin-bottom: 30px;
        font-size: 16px;
    }

    /* Card */
    .card {
        background: white;
        padding: 28px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 24px;
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6a5cff, #8b5cf6);
        color: white;
        border-radius: 12px;
        font-weight: 600;
        padding: 12px 24px;
        border: none;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(139,92,246,0.3);
    }

    /* Inputs */
    textarea, input {
        border-radius: 12px !important;
    }

    /* Question text */
    .question {
        font-weight: 600;
        color: #111827;
        margin-bottom: 8px;
    }

    </style>
    """, unsafe_allow_html=True)
