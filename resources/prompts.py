# prompts.py
"""
Prompt generation functions for all LLM-powered features in IntelliLearn.
Each function returns a prompt string customized for the specific functionality.
"""

# ------------------- STUDENT PROMPTS -------------------
def prompt_student_content(subject, learning_rate, summary):
    return (
        f"Generate adaptive study material for {subject}. "
        f"Student's learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Make content concise and challenging for high learning rate, detailed and simple for low learning rate."
    )

def prompt_student_assessment(subject, learning_rate, summary):
    return (
        f"Create an assessment for {subject}. "
        f"Student's learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Adjust difficulty and length based on learning rate."
    )

def prompt_student_doubt_solving(subject, doubt, summary):
    return (
        f"Solve the following doubt in {subject}: '{doubt}'. "
        f"ILM chat summary: {summary}. "
        "Provide a clear, step-by-step explanation."
    )

def prompt_student_insights(subject, performance_data):
    return (
        f"Analyze student performance in {subject}. "
        f"Data: {performance_data}. "
        "Highlight strengths, weaknesses, and actionable insights."
    )

def prompt_student_gamification(subject, progress):
    return (
        f"Generate gamified feedback and challenges for {subject}. "
        f"Student progress: {progress}. "
        "Suggest badges, leaderboard updates, and motivational tasks."
    )

def prompt_student_teacher_insights(subject, summary):
    return (
        f"Summarize student difficulties in {subject} for teacher. "
        f"ILM chat summary: {summary}. "
        "List topics needing attention."
    )

# ------------------- TEACHER PROMPTS -------------------
def prompt_teacher_attendance_insights(attendance_data):
    return (
        f"Analyze attendance data: {attendance_data}. "
        "Highlight patterns, anomalies, and suggest interventions."
    )

def prompt_teacher_content_generation(subject, learning_rate, summary):
    return (
        f"Generate course content for {subject}. "
        f"Target learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Ensure content is appropriate for student level."
    )

def prompt_teacher_assignment_generation(subject, learning_rate, summary):
    return (
        f"Create assignments for {subject}. "
        f"Target learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Vary complexity based on learning rate."
    )

def prompt_teacher_evaluation(assignment_data):
    return (
        f"Evaluate assignment submissions: {assignment_data}. "
        "Provide feedback and grading suggestions."
    )

def prompt_teacher_communication(message, student_summary):
    return (
        f"Draft a message to student/parent: '{message}'. "
        f"Student summary: {student_summary}. "
        "Make it clear, supportive, and actionable."
    )

# ------------------- PARENT PROMPTS -------------------
def prompt_parent_behavioral_analysis(student_data):
    return (
        f"Analyze behavioral trends for student: {student_data}. "
        "Highlight areas of concern and positive patterns."
    )

def prompt_parent_doubt_frequency(doubt_data):
    return (
        f"Summarize doubt frequency and types: {doubt_data}. "
        "Suggest ways to support the student."
    )

def prompt_parent_teacher_communication(message, teacher_summary):
    return (
        f"Draft a message to teacher: '{message}'. "
        f"Teacher summary: {teacher_summary}. "
        "Make it clear and focused on student progress."
    )

# ------------------- ILM CHAT HISTORY PROMPT -------------------
def prompt_ilm_chat_summary(chat_history):
    return (
        f"Summarize the following ILM chat history: {chat_history}. "
        "Highlight key learning moments, doubts, and progress."
    )

# ------------------- GENERAL PROMPTS -------------------
def prompt_general_leaderboard_update(leaderboard_data):
    return (
        f"Update leaderboard with data: {leaderboard_data}. "
        "Highlight top performers and recent achievements."
    )

def prompt_general_badge_award(student, badge):
    return (
        f"Award badge '{badge}' to student {student}. "
        "Explain the reason and encourage further progress."
    )

# ...add more prompt functions as new features are added...
