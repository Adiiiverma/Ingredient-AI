import streamlit as st
import pandas as pd
import os
import pytesseract
import platform

if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
import json

from PIL import Image
from reports.pdf_report import generate_pdf
from utils.groq_ai import (
    extract_ingredients_with_ai,
    analyze_with_ai,
    analyze_ingredients_with_ai
)
from utils.database import IngredientDatabase

st.set_page_config(
    page_title="IngredientAI",
    page_icon="🥗",
    layout="wide"
)
st.markdown("""
<style>

.header{
    position:fixed;
    top:0;
    left:0;
    right:0;
    height:70px;
    background:white;
    display:flex;
    align-items:center;
    padding:0 35px;
    box-shadow:0 3px 12px rgba(0,0,0,.12);
    z-index:999999;
}

.header img{
    width:42px;
    margin-right:12px;
}

.header h2{
    margin:0;
    color:#0F766E;
    font-size:30px;
    font-weight:700;
}

.block-container{
    padding-top:90px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header">

<img src="https://img.icons8.com/fluency/96/salad.png">

<h2>IngredientAI</h2>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<style>
div[data-testid="stFileUploader"]{
    border:2px dashed #16A34A !important;
    border-radius:18px !important;
    padding:25px !important;
    background:#F8FFF8 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
[data-testid="stFileUploader"]{
    background:#F8FFF8;
    border:2px dashed #16A34A;
    border-radius:20px;
    padding:35px;
}

[data-testid="stFileUploader"] section{
    border:none !important;
    background:transparent !important;
}

[data-testid="stFileUploaderDropzone"]{
    border:none !important;
    background:transparent !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div style="
background:linear-gradient(135deg,#0F766E,#16A34A);
padding:50px;
border-radius:25px;
text-align:center;
color:white;
box-shadow:0 20px 45px rgba(0,0,0,.18);
margin-bottom:35px;
">

<img src="https://img.icons8.com/fluency/160/salad.png" width="120">

<h1 style="font-size:65px;margin-top:15px;margin-bottom:10px;">
IngredientAI
</h1>

<p style="font-size:23px;opacity:.9;">
🥗 AI Powered Food Ingredient Analyzer
</p>

<p style="font-size:18px;opacity:.75;">
Upload any packaged food label and instantly receive ingredient analysis,
health score, harmful ingredient detection and AI recommendations.
</p>
            
<p style="font-size:18px;opacity:.9;">
Project by Aditya Verma
</p>            

</div>
""", unsafe_allow_html=True)

st.divider()

# ---------------- LOAD DATABASE ---------------- #

BASE_DIR = os.path.dirname(__file__)

# ---------------- FILE UPLOAD ---------------- #

st.markdown("""
<h2 style="
text-align:center;
color:#0F766E;
font-size:36px;
margin-top:15px;">
📤 Upload Food Label
</h2>

<p style="
text-align:center;
color:gray;
font-size:18px;">
Drag & Drop or Browse an image of your food label
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="upload-card">
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📷 Drag & Drop or Click to Upload",
    type=["jpg", "jpeg", "png"],
    label_visibility="visible"
)

st.markdown("""
</div>
""", unsafe_allow_html=True)
    
if uploaded_file:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 🖼 Uploaded Image")
        st.image(image,use_container_width=True)

    with col2:

        with st.spinner("🤖 Analyzing your food label..."):

            # -------- OCR -------- #

            text = pytesseract.image_to_string(image)
            
            text = text.strip()

            if len(text) < 80:
                st.error("❌ Unable to recognize the ingredients properly.")
                st.info("""
            📷 Please upload a clear image that:\n
            • Shows ONLY the ingredients lis\n
            • Is well lit\n
            • Is not blurry\n
            • Is not tilted\n
            • Contains readable text\n
            """)
                st.stop()
            st.subheader("Extracted Text")

            st.text(text)

            # -------- INGREDIENT LIST -------- #

            ingredients = extract_ingredients_with_ai(text)
            total_score = 0
            total_weight = 0

            st.divider()
            st.header("Ingredient Analysis")
            analysis = analyze_ingredients_with_ai(ingredients)

            total_score = 0

            for info in analysis:
                        
                score = info["health_score"]
                weight = 1

                total_score += score * weight
                total_weight += weight

                score = info["health_score"]

                if score >= 8:
                    color = "#d4edda"      # Green
                elif score >= 6:
                    color = "#d1ecf1"      # Blue
                elif score >= 4:
                    color = "#fff3cd"      # Yellow
                else:
                    color = "#f8d7da"      # Red
                
                st.markdown(f"""
                <div style="
                padding:20px;
                border-radius:15px;
                background:{color};
                border:1px solid #ddd;
                margin-bottom:15px;
                ">

                <h2>{info["name"]}</h2>

                <p><b>Category:</b> {info["category"]}</p>

                <p><b>Purpose:</b> {info["purpose"]}</p>

                <p><b>Description:</b> {info["description"]}</p>

                <p><b>Health Score:</b> ⭐ {info["health_score"]}/10</p>

                <p><b>Risk Level:</b> {info["risk_level"]}</p>

                <p><b>Benefits:</b> {info["benefits"]}</p>

                <p><b>Side Effects:</b> {info["side_effects"]}</p>

                <p><b>Recommendation:</b> {info["recommendation"]}</p>

                </div>
                """, unsafe_allow_html=True)

        # -------- FINAL SCORE -------- #
            overall = 0
            col1, col2, col3 = st.columns(3)

            if total_weight > 0:
            
                overall = total_score / total_weight

            with col1:
                st.metric("⭐ Health Score", f"{overall:.1f}/10")

            with col2:
                st.metric("📦 Ingredients Found", total_weight)

            with col3:
                if overall >= 8:
                    st.metric("🥗 Status", "Excellent")
                elif overall >= 6:
                    st.metric("✅ Status", "Good")
                elif overall >= 4:
                    st.metric("⚠️ Status", "Average")
                else:
                    st.metric("❌ Status", "Poor")
            st.divider()

            st.header("📊 Overall Result")
            st.progress(int(overall * 10))
            st.caption(f"Health Score: {overall*10:.0f}%")
            st.metric(
                "Overall Health Score",
                f"{overall:.1f}/10"
            )
            st.divider()

            st.header("🤖 Recommendation")

            with st.spinner("Analyzing with AI..."):
                ai_response = analyze_with_ai(text, overall)

            st.success(ai_response)

            generate_pdf(
                "IngredientAI_Report.pdf",
                overall,
                analysis,
                ai_response
            )
            
            with open("IngredientAI_Report.pdf", "rb") as pdf_file:
                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_file,
                    file_name="IngredientAI_Report.pdf",
                    mime="application/pdf"
                )

            st.divider()

        