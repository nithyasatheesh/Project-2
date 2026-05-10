# app.py

import pandas as pd
import streamlit as st

from agents.audio_summary_agent import AudioSummaryAgent
from agents.case_study_evaluator import CaseStudyEvaluator
from agents.coding_tutor_agent import CodingTutorAgent
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.summary_agent import SummaryAgent
from agents.visualization_agent import VisualizationAgent

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Multi-Agent AI Learning Platform",
    page_icon="💻",
    layout="wide"
)

st.title("💻 Multi-Agent AI Technical Learning Platform")

st.markdown("""
### Features
- Coding Tutor Agent
- Summary Agent
- Case Study Evaluator Agent
- Quiz Generator Agent
- Dataset Visualization
- Audio Learning Summaries
""")

# ---------------- INITIALIZE AGENTS ---------------- #

coding_agent = CodingTutorAgent()

summary_agent = SummaryAgent()

case_agent = CaseStudyEvaluator()

quiz_agent = QuizGeneratorAgent()

visual_agent = VisualizationAgent()

audio_agent = AudioSummaryAgent()

# ---------------- SIDEBAR ---------------- #

agent_type = st.sidebar.selectbox(
    "Select Agent",
    [
        "Coding Tutor",
        "Summary Agent",
        "Case Study Evaluator",
        "Quiz Generator"
    ]
)

# ---------------- FILE UPLOAD ---------------- #

uploaded_file = st.file_uploader(
    "📂 Upload Dataset or Code File",
    type=["csv", "txt", "py", "md"]
)

file_content = ""

df = None

if uploaded_file is not None:

    # CSV Dataset
    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

        st.success("Dataset uploaded successfully!")

        st.markdown("### 📄 Dataset Preview")

        st.dataframe(df.head())

    # Text or code file
    else:

        file_content = uploaded_file.read().decode("utf-8")

        st.markdown("### 📄 File Preview")

        st.code(file_content[:2000])

# ---------------- USER INPUT ---------------- #

user_query = st.text_area(
    "💬 Enter your question",
    height=150,
    placeholder="""
Examples:
- Explain CI/CD pipeline
- Summarize uploaded document
- Generate quiz on Spring Boot
- Detect outliers in dataset
"""
)

# ---------------- RUN AGENT ---------------- #

if st.button("🚀 Run Agent"):

    response = ""

    # ---------------- CODING TUTOR ---------------- #

    if agent_type == "Coding Tutor":

        response = coding_agent.run(user_query)

    # ---------------- SUMMARY AGENT ---------------- #

    elif agent_type == "Summary Agent":

        if file_content:

            response = summary_agent.summarize(
                file_content
            )

        else:

            response = (
                "Please upload a document or "
                "technical file for summarization."
            )

    # ---------------- CASE STUDY EVALUATOR ---------------- #

    elif agent_type == "Case Study Evaluator":

        response = case_agent.evaluate(
            user_query
        )

    # ---------------- QUIZ GENERATOR ---------------- #

    elif agent_type == "Quiz Generator":

        response = quiz_agent.generate_quiz(
            user_query
        )

    # ---------------- SHOW RESPONSE ---------------- #

    st.markdown("## 🤖 AI Response")

    st.markdown(response)

    # ---------------- VISUALIZATION ---------------- #

    if df is not None:

        # Missing values
        if "missing" in user_query.lower():

            st.markdown("## 📊 Missing Value Visualization")

            visual_agent.visualize_missing_values(df)

        # Outliers
        elif (
            "outlier" in user_query.lower()
            or "iqr" in user_query.lower()
        ):

            st.markdown("## 📊 Outlier Visualization")

            visual_agent.visualize_outliers(df)

    # ---------------- AUDIO SUMMARY ---------------- #

    st.markdown("## 🔊 Audio Learning Summary")

    audio_file, summary = (
        audio_agent.generate_audio_summary(
            response
        )
    )

    st.markdown(summary)

    if audio_file:

        audio_bytes = open(
            audio_file,
            "rb"
        ).read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )
