import streamlit as st
import fitz  # PyMuPDF
import json
import re

# Load skills from file
with open("skills.json") as f:
    SKILLS = json.load(f)

def extract_text_from_pdf(pdf_file):
    text = ""
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text.lower()

def match_skills(resume_text):
    found = {"technical": [], "soft": [], "domain": []}
    for category, skills in SKILLS.items():
        for skill in skills:
            if re.search(rf"\b{re.escape(skill)}\b", resume_text):
                found[category].append(skill)
    return found

# Streamlit UI
st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("📄 Resume Analyzer")
st.markdown("Upload your resume (PDF only) to analyze your skills.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    st.success("Resume uploaded successfully.")
    resume_text = extract_text_from_pdf(uploaded_file)
    matched = match_skills(resume_text)

    st.subheader("✅ Skills Found:")
    for category, skills in matched.items():
        st.markdown(f"**{category.capitalize()} Skills:**")
        if skills:
            st.success(", ".join(skills))
        else:
            st.warning("None found.")

    st.subheader("📌 Suggestions:")
    for category in SKILLS:
        missing = set(SKILLS[category]) - set(matched[category])
        if missing:
            st.markdown(f"*Consider learning:* {', '.join(missing)}")
            