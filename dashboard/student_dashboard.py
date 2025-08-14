import streamlit as st
from app.repo.student_repo import (
    get_student,
    get_course_contents,
    get_progress,
    get_learning_rate,
    get_leaderboard,
    add_doubt,
    get_student_badges,
    get_subject_difficulty_insights,
    generate_content_with_llm
)
from resources.prompts import ILM_PROMPT

st.title("Student Dashboard - IntelliLearn")

usn = st.text_input("Enter your USN")
if usn:
    student = get_student(usn)
    if student:
        st.header(f"Welcome, {student.get('name', usn)}")
        st.subheader("Enrolled Courses")
        course_contents = get_course_contents(usn)
        for course, contents in course_contents.items():
            st.markdown(f"**{course}**: {', '.join(contents)}")

        st.subheader("Learning Progress & Stats")
        progress = get_progress(usn)
        st.write(progress)
        st.write(f"Learning Rate: {get_learning_rate(usn)}")
        st.write(f"Badges: {get_student_badges(usn)}")

        st.subheader("Raise a Doubt")
        subject = st.selectbox("Select Subject", list(course_contents.keys()))
        doubt = st.text_area("Type your doubt")
        if st.button("Submit Doubt"):
            if add_doubt(usn, subject, doubt):
                st.success("Doubt submitted!")
            else:
                st.error("Failed to submit doubt.")

        st.subheader("Leaderboard & Gamification")
        leaderboard = get_leaderboard()
        st.table(leaderboard)

        st.subheader("Subject Difficulty Insights")
        insights = get_subject_difficulty_insights(usn)
        st.json(insights)

        st.subheader("Gemini ILM Integration (Demo)")
        st.write("Prompt sent to Gemini:")
        st.code(ILM_PROMPT)
        st.write("Gemini API response will appear here (placeholder)")

        st.subheader("Gemini ILM Interactive Content/Assessment")
        llm_input = st.text_area("Ask for content, assessment, or help (Gemini)")
        if st.button("Get LLM Response"):
            llm_response = generate_content_with_llm(usn, subject, llm_input)
            st.write("Gemini LLM Response:")
            st.success(llm_response)
    else:
        st.error("Student not found.")
