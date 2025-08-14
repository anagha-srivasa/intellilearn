import streamlit as st
from app.repo.parent_repo import (
    get_parent,
    get_children,
    get_child_data,
    get_scoring_pattern,
    get_attendance,
    get_doubt_frequency,
    get_interaction_analysis,
    get_chat_history_summary,
    get_teachers_for_child,
    add_parent_teacher_message,
    get_child_behavioral_summary,
    get_parent_report_for_child
)

st.title("Parent Dashboard - IntelliLearn")

parent_id = st.text_input("Enter your Parent ID")
if parent_id:
    parent = get_parent(parent_id)
    if parent:
        st.header(f"Welcome, {parent.get('name', parent_id)}")
        children = get_children(parent_id)
        child_usn = st.selectbox("Select Child", children)
        if child_usn:
            st.subheader("Child Monitoring")
            st.write("Scoring Pattern:", get_scoring_pattern(child_usn))
            st.write("Attendance:", get_attendance(child_usn))
            st.write("Doubt Frequency:", get_doubt_frequency(child_usn))
            st.write("Interaction Analysis:", get_interaction_analysis(child_usn))

            st.subheader("Behavioral Analysis & Report")
            st.write("Behavioral Summary:", get_child_behavioral_summary(child_usn))
            st.write("Comprehensive Report:", get_parent_report_for_child(parent_id, child_usn))

            st.subheader("Chat History Summary")
            child = get_child_data(child_usn)
            if child and 'enrolled_courses' in child:
                subject = st.selectbox("Select Subject", child['enrolled_courses'])
                st.write("Chat History Summary:", get_chat_history_summary(child_usn, subject))

            st.subheader("Parent-Teacher Communication")
            teachers = get_teachers_for_child(child_usn)
            teacher_id = st.selectbox("Select Teacher", teachers)
            message = st.text_area("Message to Teacher")
            if st.button("Send Message"):
                if add_parent_teacher_message(parent_id, teacher_id, child_usn, message):
                    st.success("Message sent!")
                else:
                    st.error("Failed to send message.")
    else:
        st.error("Parent not found.")
