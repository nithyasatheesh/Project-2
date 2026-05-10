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
# CHAT HISTORY
# ------------------------------------------------ #

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# ================================================= #
# EVALUATOR AGENT UI
# ================================================= #

if agent_type == "Evaluator Agent":

    st.markdown("# 🧪 Evaluator Agent")

    # Problem Statement

    problem_statement = st.text_area(
        "📝 Problem Statement",
        height=180,
        placeholder="""
Example:
Build a Python duplicate detection solution.
"""
    )

    # Rubric

    rubric = st.text_area(
        "📋 Evaluation Rubric",
        height=180,
        placeholder="""
1. Correctness - 40%
2. Optimization - 20%
3. Readability - 15%
4. Error Handling - 15%
5. Best Practices - 10%
"""
    )

    # Submission Upload

    uploaded_submission = st.file_uploader(
        "📂 Upload Participant Submission",
        type=[
            "txt",
            "py",
            "html",
            "pdf",
            "pptx",
            "docx",
            "csv"
        ],
        key="evaluator_upload"
    )

    submission_content = ""

    # Read file

    if uploaded_submission is not None:

        file_name = uploaded_submission.name

        st.success(f"Uploaded: {file_name}")

        # Text/code

        if (
            file_name.endswith(".txt")
            or file_name.endswith(".py")
            or file_name.endswith(".html")
        ):

            submission_content = (
                uploaded_submission.read()
                .decode("utf-8")
            )

            st.code(
                submission_content[:3000]
            )

        # CSV

        elif file_name.endswith(".csv"):

            df = pd.read_csv(
                uploaded_submission
            )

            submission_content = (
                df.head(20).to_string()
            )

            st.dataframe(df.head())

        # Binary docs

        else:

            submission_content = (
                "Binary document uploaded."
            )

    # Run Evaluation

    if st.button("🚀 Evaluate Submission"):

        if (
            not problem_statement.strip()
            or not rubric.strip()
            or not submission_content
        ):

            st.warning(
                "Please provide all evaluator inputs."
            )

        else:

            with st.spinner(
                "Evaluating submission..."
            ):

                response = evaluator_agent.evaluate(
                    problem_statement,
                    rubric,
                    submission_content
                )

            st.session_state.messages.append({
                "role": "user",
                "content":
                f"Problem Statement:\n"
                f"{problem_statement}\n\n"
                f"Rubric:\n"
                f"{rubric}"
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.markdown(
                "# 📊 Evaluation Result"
            )

            st.markdown(response)

# ================================================= #
# OTHER AGENTS
# ================================================= #

else:

    # Upload

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

    # User query

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
