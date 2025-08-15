import streamlit as st
from PyPDF2 import PdfReader
import os
from app.repo.teacher_repo import (
    get_teacher,
    get_attendance_reports,
    get_attendance_outliers,
    get_attendance_anomalies,
    get_courses,
    get_students_in_course,
    get_student_performance,
    get_student_learning_rates,
    get_topics_to_stress,
    get_approved_contents,
    approve_content,
    get_personal_assignments,
    add_personal_assignment,
    get_evaluation_mode,
    set_evaluation_mode,
    add_teacher_message,
    get_course_performance_summary,
    get_student_improvement_suggestions,
    get_teacher_activity_log,
    get_course_engagement_stats,
    save_subject_textbook
)

# Mapping: subject -> textbook text
subject_textbook_map = {}

st.title("Teacher Dashboard - IntelliLearn")

teacher_id = st.text_input("Enter your Teacher ID")
if teacher_id:
    teacher = get_teacher(teacher_id)
    if teacher:
        st.header(f"Welcome, {teacher.get('name', teacher_id)}")
        st.subheader("Upload Textbook PDF for RAG")
        rag_subject = st.selectbox("Select Subject for Textbook Upload", get_courses(teacher_id))
        uploaded_pdf = st.file_uploader("Upload Textbook PDF", type=["pdf"])
        if uploaded_pdf and rag_subject:
            pdf_reader = PdfReader(uploaded_pdf)
            textbook_text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
            subject_textbook_map[rag_subject] = textbook_text
            save_subject_textbook(rag_subject, textbook_text)
            st.success(f"Textbook uploaded and mapped to subject: {rag_subject}")
            st.write(textbook_text[:1000] + "..." if len(textbook_text) > 1000 else textbook_text)

        st.subheader("Attendance Reports & AI Insights")
        att_reports = get_attendance_reports(teacher_id)
        st.write(att_reports)
        st.write("Outliers:", get_attendance_outliers(teacher_id))
        st.write("Anomalies:", get_attendance_anomalies(teacher_id))

        st.subheader("Courses & Students")
        courses = get_courses(teacher_id)
        course = st.selectbox("Select Course", courses)
        students = get_students_in_course(teacher_id, course)
        st.write(f"Students in {course}: {students}")
        st.write("Performance:", get_student_performance(teacher_id, course))
        st.write("Learning Rates:", get_student_learning_rates(teacher_id, course))
        st.write("Topics to Stress:", get_topics_to_stress(teacher_id))

        st.subheader("Content Approval & Delivery")
        approved = get_approved_contents(teacher_id, course)
        st.write(f"Approved Contents for {course}: {approved}")
        new_content = st.text_input("Content to Approve")
        if st.button("Approve Content"):
            if approve_content(teacher_id, course, new_content):
                st.success("Content approved!")
            else:
                st.error("Failed to approve content.")

        st.subheader("Assignments")
        assignments = get_personal_assignments(teacher_id, course)
        st.write(f"Assignments for {course}: {assignments}")
        new_assignment = st.text_input("Add Assignment")
        if st.button("Add Assignment"):
            if add_personal_assignment(teacher_id, course, new_assignment):
                st.success("Assignment added!")
            else:
                st.error("Failed to add assignment.")

        st.subheader("Evaluation Mode")
        mode = get_evaluation_mode(teacher_id, course)
        st.write(f"Current Mode: {mode}")
        new_mode = st.selectbox("Set Evaluation Mode", ["manual", "ilm"])
        if st.button("Set Mode"):
            if set_evaluation_mode(teacher_id, course, new_mode):
                st.success("Evaluation mode updated!")
            else:
                st.error("Failed to update mode.")

        st.subheader("Communication")
        comm_type = st.radio("Message Type", ["Class", "Student"])
        message = st.text_area("Message")
        student_usn = st.text_input("Student USN (if individual)") if comm_type == "Student" else None
        if st.button("Send Message"):
            if add_teacher_message(teacher_id, course, message, to_class=(comm_type=="Class"), student_usn=student_usn):
                st.success("Message sent!")
            else:
                st.error("Failed to send message.")

        st.subheader("Analytics & Insights")
        st.write("Course Performance Summary:", get_course_performance_summary(teacher_id, course))
        st.write("Student Improvement Suggestions:", get_student_improvement_suggestions(teacher_id, course))
        st.write("Teacher Activity Log:", get_teacher_activity_log(teacher_id))
        st.write("Course Engagement Stats:", get_course_engagement_stats(teacher_id, course))

        st.subheader("Gemini ILM Integration (Demo)")
        st.write("Prompt sent to Gemini:")
        rag_text = subject_textbook_map.get(course, "")
        st.write(f"RAG Context for {course}: {rag_text[:500]}..." if rag_text else "No textbook uploaded for this subject.")
        st.write("Gemini API response will appear here (placeholder)")

        st.subheader("Gemini ILM Interactive Tasks with RAG")
        llm_task = st.selectbox("Select LLM Task", ["Doubt Solving", "Assignment Generation", "Evaluation", "Content Generation"])
        llm_input = st.text_area("Enter your query or prompt for Gemini")
        rag_text = subject_textbook_map.get(course, "")
        if st.button("Run Gemini LLM with RAG Context"):
            if not rag_text:
                st.error("No textbook uploaded for this subject. Please upload a PDF first.")
            else:
                # Example: Combine prompt and RAG context for LLM
                from llm.llm_client import run_gemini_llm
                full_context = f"RAG textbook context:\n{rag_text[:2000]}"  # Limit context size for demo
                response = run_gemini_llm(llm_input, full_context)
                st.write("Gemini LLM Response:")
                st.success(response)
    else:
        st.error("Teacher not found.")
