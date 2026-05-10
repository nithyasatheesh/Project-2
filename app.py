import pandas as pd

    # Coding Tutor
    if agent_type == "Coding Tutor":

        response = coding_agent.run(user_query)

    # Summary Agent
    elif agent_type == "Summary Agent":

        response = summary_agent.summarize(file_content)

    # Case Study Evaluator
    elif agent_type == "Case Study Evaluator":

        response = case_agent.evaluate(user_query)

    # Quiz Generator
    elif agent_type == "Quiz Generator":

        response = quiz_agent.generate_quiz(user_query)

    # ---------------- RESPONSE ---------------- #

    st.markdown("## AI Response")

    st.markdown(response)

    # ---------------- VISUALIZATION ---------------- #

    if df is not None:

        if "missing" in user_query.lower():
            visual_agent.visualize_missing_values(df)

        if "outlier" in user_query.lower():
            visual_agent.visualize_outliers(df)

    # ---------------- AUDIO SUMMARY ---------------- #

    st.markdown("## Audio Learning Summary")

    audio_file, summary = audio_agent.generate_audio_summary(
        response
    )

    st.markdown(summary)

    audio_bytes = open(audio_file, "rb").read()

    st.audio(audio_bytes, format="audio/mp3")
