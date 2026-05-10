# app.py

import pandas as pd
import streamlit as st
import PyPDF2

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

    st.session_state.quiz_data = None

    st.session_state.quiz_answers = {}

    st.session_state.messages = []

    st.session_state.last_agent = agent_type

    st.rerun()

# ------------------------------------------------ #
# CHAT HISTORY
# ------------------------------------------------ #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ------------------------------------------------ #
# FILE HELPERS
# ------------------------------------------------ #

def read_text_file(file):

    return file.read().decode("utf-8")


def read_pdf_file(file):

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text

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
    )

    uploaded_rubric = st.file_uploader(
        "📂 Upload Rubric",
        type=[
            "txt",
            "pdf",
            "csv",
            "xlsx"
        ],
        key="rubric_upload"
    )

    # ------------------------------------------------ #
    # PARTICIPANT SUBMISSION
    # ------------------------------------------------ #

    participant_submission = st.text_area(
        "💻 Type Participant Submission (Optional)",
        height=250
    )

    uploaded_submission = st.file_uploader(
        "📂 Upload Participant Submission",
        type=[
            "txt",
            "py",
            "html",
            "sql",
            "csv",
            "xlsx"
        ],
        key="submission_upload"
    )

    # ------------------------------------------------ #
    # OPTIONAL DATASET
    # ------------------------------------------------ #

    uploaded_dataset = st.file_uploader(
        "📊 Optional Dataset Upload",
        type=[
            "csv",
            "xlsx"
        ],
        key="dataset_upload"
    )

    dataset_info = ""

    # ------------------------------------------------ #
    # PROCESS PROBLEM STATEMENT
    # ------------------------------------------------ #

    if uploaded_problem is not None:

        # TXT / PY / HTML

        if (
            uploaded_problem.name.endswith(".txt")
            or uploaded_problem.name.endswith(".py")
            or uploaded_problem.name.endswith(".html")
        ):

            problem_statement += (
                "\n\n"
                + read_text_file(uploaded_problem)
            )

        # PDF

        elif uploaded_problem.name.endswith(".pdf"):

            problem_statement += (
                "\n\n"
                + read_pdf_file(uploaded_problem)
            )

        st.markdown("## 📄 Problem Statement Preview")

        st.text(problem_statement[:3000])

    # ------------------------------------------------ #
    # PROCESS RUBRIC
    # ------------------------------------------------ #

    if uploaded_rubric is not None:

        # TXT

        if uploaded_rubric.name.endswith(".txt"):

            rubric += (
                "\n\n"
                + read_text_file(uploaded_rubric)
            )

        # PDF

        elif uploaded_rubric.name.endswith(".pdf"):

            rubric += (
                "\n\n"
                + read_pdf_file(uploaded_rubric)
            )

        # CSV

        elif uploaded_rubric.name.endswith(".csv"):

            rubric_df = pd.read_csv(
                uploaded_rubric
            )

            st.dataframe(rubric_df)

            rubric += (
                "\n\n"
                + rubric_df.to_string()
            )

        # XLSX

        elif uploaded_rubric.name.endswith(".xlsx"):

            rubric_df = pd.read_excel(
                uploaded_rubric
            )

            st.dataframe(rubric_df)

            rubric += (
                "\n\n"
                + rubric_df.to_string()
            )

        st.markdown("## 📋 Rubric Preview")

        st.text(rubric[:3000])

    # ------------------------------------------------ #
    # PROCESS PARTICIPANT SUBMISSION
    # ------------------------------------------------ #

    if uploaded_submission is not None:

        file_name = uploaded_submission.name

        # TXT / PY / HTML / SQL

        if (
            file_name.endswith(".txt")
            or file_name.endswith(".py")
            or file_name.endswith(".html")
            or file_name.endswith(".sql")
        ):

            participant_submission += (
                "\n\n"
                + read_text_file(uploaded_submission)
            )

            st.code(
                participant_submission[:3000]
            )

        # CSV

        elif file_name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_submission
            )

            st.dataframe(df.head())

            participant_submission += (
                "\n\nDataset Preview:\n"
                + df.head(20).to_string()
            )

        # XLSX

        elif file_name.endswith(".xlsx"):

            df = pd.read_excel(
                uploaded_submission
            )

            st.dataframe(df.head())

            participant_submission += (
                "\n\nExcel Preview:\n"
                + df.head(20).to_string()
            )

    # ------------------------------------------------ #
    # OPTIONAL DATASET
    # ------------------------------------------------ #

    if uploaded_dataset is not None:

        if uploaded_dataset.name.endswith(".csv"):

            dataset_df = pd.read_csv(
                uploaded_dataset
            )

        else:

            dataset_df = pd.read_excel(
                uploaded_dataset
            )

        st.markdown("## 📊 Dataset Preview")

        st.dataframe(dataset_df.head())

        dataset_info = dataset_df.describe(
            include="all"
        ).to_string()

    # ------------------------------------------------ #
    # RUN EVALUATION
    # ------------------------------------------------ #

    if st.button("🚀 Evaluate Submission"):

        if not problem_statement.strip():

            st.warning(
                "Please provide problem statement."
            )

        elif not rubric.strip():

            st.warning(
                "Please provide rubric."
            )

        elif not participant_submission.strip():

            st.warning(
                "Please provide participant submission."
            )

        else:

            with st.spinner(
                "Evaluating submission..."
            ):

                response = evaluator_agent.evaluate(
                    problem_statement,
                    rubric,
                    participant_submission,
                    dataset_info
                )

            st.markdown(
                "# 📊 Evaluation Result"
            )

            st.markdown(response)

            # Audio Summary

            st.markdown(
                "## 🔊 Audio Learning Summary"
            )

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

# ================================================= #
# OTHER AGENTS
# ================================================= #

else:

    uploaded_file = st.file_uploader(
        "📂 Upload Dataset or Code File",
        type=["csv", "txt", "py", "md"]
    )

    file_content = ""

    df = None

    if uploaded_file is not None:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

            st.dataframe(df.head())

        else:

            file_content = (
                uploaded_file.read()
                .decode("utf-8")
            )

            st.code(file_content[:2000])

    user_query = st.text_area(
        "💬 Enter your question",
        height=150
    )

    if st.button("🚀 Run Agent"):

        response = ""

        if agent_type == "Coding Tutor":

            response = coding_agent.run(
                user_query
            )

        elif agent_type == "Summary Agent":

            if file_content:

                response = summary_agent.summarize(
                    file_content
                )

            else:

                response = (
                    "Please upload document."
                )

        elif agent_type == "Quiz Generator":

            quiz_data = quiz_agent.generate_quiz(
                user_query
            )

            st.session_state.quiz_data = quiz_data

            response = (
                f"Quiz generated on: {user_query}"
            )

        st.session_state.messages.append({
            "role": "user",
            "content": user_query
        })

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

            if user_answer == correct_answer:

                score += 1

                st.success(
                    f"Q{i+1}: Correct"
                )

            else:

                st.error(
                    f"Q{i+1}: Incorrect"
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
