# prompts.py
"""
Prompt generation functions for all LLM-powered features in IntelliLearn.
Each function returns a prompt string customized for the specific functionality, with detailed instructions for Gemini and RAG context.
"""

# ------------------- STUDENT PROMPTS -------------------
def prompt_student_content(subject, learning_rate, summary, rag_context=None):
    base = (
        f"You are an adaptive learning assistant for the subject {subject}. "
        f"Student's learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Generate study material that matches the student's learning rate: concise and challenging for high, detailed and simple for low. "
        "If RAG context is provided, use the textbook content to ensure accuracy and relevance. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_student_assessment(subject, learning_rate, summary, rag_context=None):
    base = (
        f"Create a personalized assessment for {subject}. "
        f"Student's learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Adjust difficulty and length based on learning rate. "
        "Use textbook content for question accuracy if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_student_doubt_solving(subject, doubt, summary, rag_context=None):
    base = (
        f"Solve the following doubt in {subject}: '{doubt}'. "
        f"ILM chat summary: {summary}. "
        "Provide a clear, step-by-step explanation. "
        "If textbook content is available, use it to support your answer. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_student_insights(subject, performance_data, rag_context=None):
    base = (
        f"Analyze student performance in {subject}. "
        f"Data: {performance_data}. "
        "Highlight strengths, weaknesses, and actionable insights. "
        "Use textbook context for deeper analysis if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_student_gamification(subject, progress, rag_context=None):
    base = (
        f"Generate gamified feedback and challenges for {subject}. "
        f"Student progress: {progress}. "
        "Suggest badges, leaderboard updates, and motivational tasks. "
        "If textbook content is available, use it to create context-aware challenges. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_student_teacher_insights(subject, summary, rag_context=None):
    base = (
        f"Summarize student difficulties in {subject} for teacher. "
        f"ILM chat summary: {summary}. "
        "List topics needing attention. "
        "Use textbook context for more precise recommendations if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

# ------------------- TEACHER PROMPTS -------------------
def prompt_teacher_attendance_insights(attendance_data, rag_context=None):
    base = (
        f"Analyze attendance data: {attendance_data}. "
        "Highlight patterns, anomalies, and suggest interventions. "
        "If textbook context is available, relate attendance to content engagement. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_teacher_content_generation(subject, learning_rate, summary, rag_context=None):
    base = (
        f"Generate course content for {subject}. "
        f"Target learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Ensure content is appropriate for student level. "
        "Use textbook content for accuracy and completeness. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_teacher_assignment_generation(subject, learning_rate, summary, rag_context=None):
    base = (
        f"Create assignments for {subject}. "
        f"Target learning rate: {learning_rate}. "
        f"ILM chat summary: {summary}. "
        "Vary complexity based on learning rate. "
        "Use textbook content for question generation if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_teacher_evaluation(assignment_data, rag_context=None):
    base = (
        f"Evaluate assignment submissions: {assignment_data}. "
        "Provide feedback and grading suggestions. "
        "Use textbook context for reference if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_teacher_communication(message, student_summary, rag_context=None):
    base = (
        f"Draft a message to student/parent: '{message}'. "
        f"Student summary: {student_summary}. "
        "Make it clear, supportive, and actionable. "
        "Use textbook context for additional guidance if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

# ------------------- PARENT PROMPTS -------------------
def prompt_parent_behavioral_analysis(student_data, rag_context=None):
    base = (
        f"Analyze behavioral trends for student: {student_data}. "
        "Highlight areas of concern and positive patterns. "
        "Use textbook context for deeper understanding if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_parent_doubt_frequency(doubt_data, rag_context=None):
    base = (
        f"Summarize doubt frequency and types: {doubt_data}. "
        "Suggest ways to support the student. "
        "Use textbook context for more targeted advice if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_parent_teacher_communication(message, teacher_summary, rag_context=None):
    base = (
        f"Draft a message to teacher: '{message}'. "
        f"Teacher summary: {teacher_summary}. "
        "Make it clear and focused on student progress. "
        "Use textbook context for additional support if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

# ------------------- ILM CHAT HISTORY PROMPT -------------------
def prompt_ilm_chat_summary(chat_history, rag_context=None):
    base = (
        f"Summarize the following ILM chat history: {chat_history}. "
        "Highlight key learning moments, doubts, and progress. "
        "Use textbook context for more accurate summary if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

# ------------------- GENERAL PROMPTS -------------------
def prompt_general_leaderboard_update(leaderboard_data, rag_context=None):
    base = (
        f"Update leaderboard with data: {leaderboard_data}. "
        "Highlight top performers and recent achievements. "
        "Use textbook context for additional insights if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

def prompt_general_badge_award(student, badge, rag_context=None):
    base = (
        f"Award badge '{badge}' to student {student}. "
        "Explain the reason and encourage further progress. "
        "Use textbook context for more meaningful feedback if available. "
    )
    if rag_context:
        base += f"Reference textbook content: {rag_context[:500]}... "
    return base

# ...add more prompt functions as new features are added...
