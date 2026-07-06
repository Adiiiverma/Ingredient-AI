import streamlit as st

def load_css():
    st.markdown("""
    <style>

    .main{
        background:#f5f7fb;
    }

    .title{
        font-size:52px;
        font-weight:bold;
        color:#2E8B57;
        text-align:center;
    }

    .subtitle{
        text-align:center;
        color:#666;
        font-size:20px;
        margin-bottom:25px;
    }

    .card{
        background:white;
        padding:20px;
        border-radius:15px;
        box-shadow:0 4px 15px rgba(0,0,0,0.12);
        margin-bottom:15px;
    }

    .safe{
        border-left:8px solid #2ecc71;
    }

    .moderate{
        border-left:8px solid orange;
    }

    .bad{
        border-left:8px solid red;
    }

    </style>
    """, unsafe_allow_html=True)