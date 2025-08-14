import streamlit as st
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
    get_course_engagement_stats
)
from resources.prompts import ILM_PROMPT

st.title("Teacher Dashboard - IntelliLearn")

teacher_id = st.text_input("Enter your Teacher ID")
if teacher_id:
    teacher = get_teacher(teacher_id)
    if teacher:
        st.header(f"Welcome, {teacher.get('name', teacher_id)}")
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
        st.code(ILM_PROMPT)
        st.write("Gemini API response will appear here (placeholder)")
    else:
        st.error("Teacher not found.")
