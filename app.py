# Enhanced Interactive AI Resume Optimizer - app.py
import streamlit as st
from resume_parser.parser import extract_resume_text
from ai_services.cover_letter import generate_cover_letter
from ai_services.job_fit_score import calculate_fit_score
from time import sleep

# Page Configuration
st.set_page_config(page_title="AI Resume Optimizer", page_icon="🤖", layout="wide")

# Funky Interactive Custom CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Roboto:wght@400;700&display=swap');

body { font-family: 'Roboto', sans-serif; }

.title {
    font-family: 'Poppins', sans-serif;
    color: #FF6F61;
    text-shadow: 2px 2px #FFD700;
    font-size: 50px;
    animation: bounce 1s ease-in-out;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
  40% {transform: translateY(-20px);}
  60% {transform: translateY(-10px);}
}

.stButton>button {
    background: linear-gradient(45deg, #FF6F61, #FFC300);
    color: #FFFFFF;
    border-radius: 20px;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.1);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.keywords-box {
    background: linear-gradient(135deg, #FF6F61, #FFC300);
    color: #FFFFFF;
    border-radius: 10px;
    padding: 10px;
    font-size: 16px;
}

.metric-box {
    font-size: 30px;
    color: #FF6F61;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Funky Animated Title
st.markdown('<h1 class="title">🚀 AI Resume Optimizer 🤖</h1>', unsafe_allow_html=True)
st.markdown('### Level Up Your Job Hunt with AI Magic! 🌟')

# Sidebar
with st.sidebar:
    st.header("✨ Navigate")
    page = st.radio("", ["Resume Analyzer", "Cover Letter Magic"], label_visibility="collapsed")
    st.write("---")
    st.info("Upload your files and let AI do the magic! 🎩")

# Main Content
if page == "Resume Analyzer":
    st.subheader("📈 Resume Analyzer")
    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"])
    with col2:
        job_desc = st.text_area("📌 Paste Job Description", height=160)

    if st.button("✨ Analyze!", use_container_width=True):
        if resume_file and job_desc:
            with st.spinner("Analyzing your career spells... 🧙‍♂️"):
                sleep(1)
                resume_text = extract_resume_text(resume_file)
                score, keywords = calculate_fit_score(resume_text, job_desc)

            st.markdown(f"<div class='metric-box'>🔥 Match Score: {score}%</div>", unsafe_allow_html=True)

            keyword_highlight = ', '.join([f"🌟 <b>{kw}</b>" for kw in keywords])
            st.markdown(f"<div class='keywords-box'>🎯 Top Keywords: {keyword_highlight}</div>", unsafe_allow_html=True)

            if score < 50:
                st.warning("🚨 Your resume could use some magic! Consider adding these keywords.")
            else:
                st.success("🎉 Great match! You're ready to conquer!")
        else:
            st.error("🛑 Please upload your resume and job description!")

elif page == "Cover Letter Magic":
    st.subheader("📝 Cover Letter Magic")
    col1, col2 = st.columns(2)

    with col1:
        resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx"], key="cover_letter")
    with col2:
        job_desc = st.text_area("📌 Paste Job Description", height=160, key="job_cover")

    tone = st.selectbox("🎨 Choose Your Cover Letter Tone:", ["Professional", "Friendly", "Enthusiastic", "Concise"])

    if st.button("✨ Craft My Letter!", use_container_width=True):
        if resume_file and job_desc:
            with st.spinner("Brewing your cover letter potion... 🧪"):
                sleep(1)
                resume_text = extract_resume_text(resume_file)
                cover_letter = generate_cover_letter(resume_text, job_desc, tone.lower())

            st.markdown("### 💌 Your AI-Powered Cover Letter:")
            st.text_area("", value=cover_letter, height=300)
            st.download_button("📥 Download Letter", cover_letter, "cover_letter.txt")
        else:
            st.error("🛑 Please upload your resume and job description!")
