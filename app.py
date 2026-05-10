
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

# ---------------- AGENTS ---------------- #

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
    st.audio(audio_bytes, format="audio/mp3")
