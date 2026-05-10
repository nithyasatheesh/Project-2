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
- Case Study Evaluator
- Interactive Quiz Generator
- Dataset Visualization
- Audio Learning Summary
""")

# ---------------- INITIALIZE AGENTS ---------------- #

coding_agent = CodingTutorAgent()

summary_agent = SummaryAgent()

case_agent = CaseStudyEvaluator()

quiz_agent = QuizGeneratorAgent()

visual_agent = VisualizationAgent()

audio_agent = AudioSummaryAgent()

# ---------------- SESSION STATE ---------------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

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

# ---------------- CHAT HISTORY ---------------- #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

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

        st.markdown("## 📄 Dataset Preview")

        st.dataframe(df.head())

    # Text or code file
    else:

        file_content = uploaded_file.read().decode("utf-8")

        st.markdown("## 📄 File Preview")

        st.code(file_content[:2000])

# ---------------- USER INPUT ---------------- #

user_query = st.text_area(
    "💬 Enter your question",
    height=150,
    placeholder="""
Examples:
- Explain CI/CD pipeline
- Summarize uploaded document
- Evaluate my SQL solution
- Generate quiz on Spring Boot
"""
)

# ---------------- RUN AGENT ---------------- #

if st.button("🚀 Run Agent"):

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    response = ""

    # ---------------- CODING TUTOR ---------------- #

    if agent_type == "Coding Tutor":

        response = coding_agent.run(user_query)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # ---------------- SUMMARY AGENT ---------------- #

    elif agent_type == "Summary Agent":

        if file_content:

            response = summary_agent.summarize(
                file_content
            )

        else:

            response = (
                "Please upload a document "
                "for summarization."
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # ---------------- CASE STUDY EVALUATOR ---------------- #

    elif agent_type == "Case Study Evaluator":

        response = case_agent.evaluate(
            user_query
        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # ---------------- QUIZ GENERATOR ---------------- #

    elif agent_type == "Quiz Generator":

        quiz_data = quiz_agent.generate_quiz(
            user_query
        )

        st.session_state.quiz_data = quiz_data

        st.session_state.messages.append({
            "role": "assistant",
            "content":
            f"Interactive quiz generated on: {user_query}"
        })

    st.rerun()

# ---------------- DISPLAY QUIZ ---------------- #

if (
    agent_type == "Quiz Generator"
    and st.session_state.quiz_data
):

    st.markdown("# 🧠 Interactive Quiz")

    for i, question_data in enumerate(
        st.session_state.quiz_data
    ):

        st.markdown(
            f"## Q{i+1}. "
            f"{question_data['question']}"
        )

        options = question_data["options"]

        selected = st.radio(
            "Choose your answer",
            [
                f"A. {options['A']}",
                f"B. {options['B']}",
                f"C. {options['C']}",
                f"D. {options['D']}"
            ],
            key=f"quiz_{i}"
        )

        selected_letter = selected[0]

        st.session_state.quiz_answers[i] = (
            selected_letter
        )

    # ---------------- SUBMIT QUIZ ---------------- #

    if st.button("✅ Submit Quiz"):

        score = 0

        st.markdown("# 🎯 Quiz Results")

        for i, question_data in enumerate(
            st.session_state.quiz_data
        ):

            correct_answer = (
                question_data["correct_answer"]
            )

            explanation = (
                question_data["explanation"]
            )

            user_answer = (
                st.session_state.quiz_answers[i]
            )

            st.markdown(
                f"## Q{i+1}: "
                f"{question_data['question']}"
            )

            st.markdown(
                f"Your Answer: {user_answer}"
            )

            st.markdown(
                f"Correct Answer: {correct_answer}"
            )

            # Correct answer
            if user_answer == correct_answer:

                score += 1

                st.success("✅ Correct")

            # Incorrect answer
            else:

                st.error("❌ Incorrect")

            st.markdown(
                f"Explanation: {explanation}"
            )

            st.markdown("---")

        # ---------------- FINAL SCORE ---------------- #

        st.markdown(
            f"# 🏆 Final Score: {score}/5"
        )

        if score == 5:

            st.success(
                "Excellent technical understanding!"
            )

        elif score >= 3:

            st.info(
                "Good attempt. Review explanations."
            )

        else:

            st.warning(
                "Need more practice on this topic."
            )

# ---------------- VISUALIZATION ---------------- #

if df is not None:

    if "missing" in user_query.lower():

        st.markdown("## 📊 Missing Values")

        visual_agent.visualize_missing_values(df)

    elif (
        "outlier" in user_query.lower()
        or "iqr" in user_query.lower()
    ):

        st.markdown("## 📊 Outlier Detection")

        visual_agent.visualize_outliers(df)

# ---------------- AUDIO SUMMARY ---------------- #

if (
    len(st.session_state.messages) > 0
    and agent_type != "Quiz Generator"
):

    latest_response = (
        st.session_state.messages[-1]["content"]
    )

    st.markdown("## 🔊 Audio Learning Summary")

    audio_file, summary = (
        audio_agent.generate_audio_summary(
            latest_response
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
