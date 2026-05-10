# app.py

import pandas as pd
import streamlit as st

from agents.audio_summary_agent import AudioSummaryAgent
from agents.evaluator_agent import EvaluatorAgent
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

case_agent = EvaluatorAgent()

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

    # ----------------  EVALUATOR ---------------- #

  # ---------------- EVALUATOR AGENT ---------------- #

elif agent_type == "Evaluator Agent":

    st.markdown("# 🧪 Evaluator Agent")

    problem_statement = st.text_area(
        "📝 Problem Statement",
        height=180,
        placeholder="""
Example:
Write a Python function to detect duplicates in a list.
The solution should be optimized.
"""
    )

    participant_solution = st.text_area(
        "💻 Participant Solution",
        height=300,
        placeholder="""
Paste participant code here
"""
    )

    if st.button("🚀 Evaluate Solution"):

        # Validation
        if (
            not problem_statement.strip()
            or not participant_solution.strip()
        ):

            st.warning(
                "Please provide both inputs."
            )

        else:

            with st.spinner(
                "Evaluating solution..."
            ):

                response = evaluator_agent.evaluate(
                    problem_statement,
                    participant_solution
                )

            # Store chat history
            st.session_state.messages.append({
                "role": "user",
                "content":
                f"Problem:\n{problem_statement}\n\n"
                f"Solution:\n{participant_solution}"
            })

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            # DISPLAY RESPONSE
            st.markdown("# 📊 Evaluation Result")

            st.markdown(response)

            # ---------------- AUDIO SUMMARY ---------------- #

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

# UPDATED QUIZ SECTION IN app.py

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

        # ---------------- RADIO BUTTON ---------------- #

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

    # ---------------- SUBMIT QUIZ ---------------- #

    if st.button("✅ Submit Quiz"):

        # ---------------- VALIDATION ---------------- #

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

        # ---------------- SCORING ---------------- #

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

            # ---------------- CORRECT ---------------- #

            if user_answer == correct_answer:

                score += 1

                st.success("✅ Correct")

            # ---------------- INCORRECT ---------------- #

            else:

                st.error("❌ Incorrect")

            st.markdown(
                f"Explanation: {explanation}"
            )

            st.markdown("---")

        # ---------------- FINAL SCORE ---------------- #

        st.markdown(
            f"# 🏆 Final Score: "
            f"{score}/5"
        )

        # ---------------- FEEDBACK ---------------- #

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
