# app.py

import pandas as pd
import streamlit as st

from agents.audio_summary_agent import AudioSummaryAgent
from agents.coding_tutor_agent import CodingTutorAgent
from agents.evaluator import EvaluatorAgent
from agents.quiz_generator_agent import QuizGeneratorAgent
from agents.summary_agent import SummaryAgent
from agents.visualization_agent import VisualizationAgent

# ------------------------------------------------ #
# PAGE CONFIG
# ------------------------------------------------ #

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
- Evaluator Agent
- Interactive Quiz Generator
- Dataset Visualization
- Audio Learning Summary
""")

# ------------------------------------------------ #
# INITIALIZE AGENTS
# ------------------------------------------------ #

coding_agent = CodingTutorAgent()

summary_agent = SummaryAgent()

evaluator_agent = EvaluatorAgent()

quiz_agent = QuizGeneratorAgent()

visual_agent = VisualizationAgent()

audio_agent = AudioSummaryAgent()

# ------------------------------------------------ #
# SESSION STATE
# ------------------------------------------------ #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}

# ------------------------------------------------ #
# SIDEBAR
# ------------------------------------------------ #

agent_type = st.sidebar.selectbox(
    "Select Agent",
    [
        "Coding Tutor",
        "Summary Agent",
        "Evaluator Agent",
        "Quiz Generator"
    ]
)

# ------------------------------------------------ #
# AGENT SWITCH HANDLER
# ------------------------------------------------ #

if "last_agent" not in st.session_state:

    st.session_state.last_agent = agent_type

if st.session_state.last_agent != agent_type:

    # Clear quiz state
    st.session_state.quiz_data = None

    st.session_state.quiz_answers = {}

    # Clear chat history
    st.session_state.messages = []

    # Update selected agent
    st.session_state.last_agent = agent_type

    # Refresh UI
    st.rerun()

# ------------------------------------------------ #
# CHAT HISTORY
# ------------------------------------------------ #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ================================================= #
# EVALUATOR AGENT
# ================================================= #

# ================================================= #
# EVALUATOR AGENT
# ================================================= #

if agent_type == "Evaluator Agent":

    st.markdown("# 🧪 Evaluator Agent")

    # ------------------------------------------------ #
    # PROBLEM STATEMENT
    # ------------------------------------------------ #

    problem_statement = st.text_area(
        "📝 Type Problem Statement (Optional)",
        height=180
    )

    uploaded_problem = st.file_uploader(
        "📂 Upload Problem Statement",
        type=[
            "txt",
            "py",
            "html",
            "pdf",
            "docx"
        ],
        key="problem_upload"
    )

    # ------------------------------------------------ #
    # RUBRIC
    # ------------------------------------------------ #

    rubric = st.text_area(
        "📋 Type Evaluation Rubric (Optional)",
        height=180
            st.markdown(response)
# ================================================= #
# OTHER AGENTS
# ================================================= #

else:

    # Upload file

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset or Code File",
        type=["csv", "txt", "py", "md"]
    )

    file_content = ""

    df = None

    if uploaded_file is not None:

        # CSV

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            st.dataframe(df.head())

        # Text/code

        else:

            file_content = (
                uploaded_file.read()
                .decode("utf-8")
            )

            st.code(file_content[:2000])

    # User Query

    user_query = st.text_area(
        "💬 Enter your question",
        height=150,
        placeholder="""
Examples:
- Explain CI/CD pipeline
- Summarize uploaded document
- Generate quiz on Spring Boot
"""
    )

    # Run Agent

    if st.button("🚀 Run Agent"):

        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

        response = ""

        # Coding Tutor

        if agent_type == "Coding Tutor":

            response = coding_agent.run(
                user_query
            )

        # Summary Agent

        elif agent_type == "Summary Agent":

            if file_content:

                response = summary_agent.summarize(
                    file_content
                )

            else:

                response = (
                    "Please upload a document."
                )

        # Quiz Generator

        elif agent_type == "Quiz Generator":

            quiz_data = quiz_agent.generate_quiz(
                user_query
            )

            st.session_state.quiz_data = quiz_data

            response = (
                f"Quiz generated on: {user_query}"
            )

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

# ================================================= #
# QUIZ DISPLAY
# ================================================= #

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
                "Select an option",
                f"A. {options['A']}",
                f"B. {options['B']}",
                f"C. {options['C']}",
                f"D. {options['D']}"
            ],
            index=0,
            key=f"quiz_{i}"
        )

        selected_letter = None

        if selected != "Select an option":

            selected_letter = selected[0]

        st.session_state.quiz_answers[i] = (
            selected_letter
        )

    # Submit Quiz

    if st.button("✅ Submit Quiz"):

        unanswered = []

        for i in range(
            len(st.session_state.quiz_data)
        ):

            if (
                st.session_state.quiz_answers.get(i)
                is None
            ):

                unanswered.append(i + 1)

        if unanswered:

            st.warning(
                f"Please answer all questions. "
                f"Missing: {unanswered}"
            )

            st.stop()

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

            if user_answer == correct_answer:

                score += 1

                st.success(
                    f"✅ Correct"
                )

            else:

                st.error(
                    f"❌ Incorrect"
                )

            st.markdown(
                f"Correct Answer: {correct_answer}"
            )

            st.markdown(
                f"Explanation: {explanation}"
            )

            st.markdown("---")

        st.markdown(
            f"# 🏆 Final Score: {score}/5"
        )

# ================================================= #
# VISUALIZATION
# ================================================= #

if (
    agent_type == "Coding Tutor"
    and 'df' in locals()
    and df is not None
):

    if "missing" in user_query.lower():

        st.markdown("## 📊 Missing Values")

        visual_agent.visualize_missing_values(df)

    elif (
        "outlier" in user_query.lower()
        or "iqr" in user_query.lower()
    ):

        st.markdown("## 📊 Outlier Detection")

        visual_agent.visualize_outliers(df)

# ================================================= #
# AUDIO SUMMARY
# ================================================= #

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
