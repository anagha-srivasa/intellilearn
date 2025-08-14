import os
import json
from typing import Any, Dict, List, Optional
import tempfile
import yaml
from llm.llm_client import create_llm_client
from resources.prompts import (
    prompt_student_content,
    prompt_student_assessment,
    prompt_student_doubt_solving,
    prompt_student_insights,
    prompt_student_gamification,
    prompt_student_teacher_insights,
    prompt_ilm_chat_summary,
    prompt_general_leaderboard_update,
    prompt_general_badge_award
)

# Dynamically resolve project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'students')
ILM_HISTORY_PATH = os.path.join(PROJECT_ROOT, 'db', 'ilm_history')
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.yml')
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(ILM_HISTORY_PATH, exist_ok=True)

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)
GEMINI_API_KEY = config['llm']['gemini_api_key']

def get_student(usn: str) -> Optional[Dict[str, Any]]:
    """Fetch student data by USN. Returns None if not found or error."""
    path = os.path.join(DB_PATH, f"{usn}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading student file {path}: {e}")
    return None


def save_student(usn: str, data: Dict[str, Any]) -> bool:
    """Save student data by USN. Returns True if successful."""
    path = os.path.join(DB_PATH, f"{usn}.json")
    try:
        # Atomic write
        with tempfile.NamedTemporaryFile("w", delete=False, dir=DB_PATH, encoding="utf-8") as tf:
            json.dump(data, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving student file {path}: {e}")
        return False


def get_learning_rate(usn: str) -> int:
    """Get student's learning rate (int, 1-100). Returns 50 if not found."""
    student = get_student(usn)
    lr = student.get('learning_rate') if student else None
    if isinstance(lr, int) and 1 <= lr <= 100:
        return lr
    return 50


def update_learning_rate(usn: str, new_rate: int) -> bool:
    """Update and persist student's learning rate. Returns True if successful."""
    if not (1 <= new_rate <= 100):
        print(f"Invalid learning rate: {new_rate}")
        return False
    student = get_student(usn)
    if student:
        student['learning_rate'] = new_rate
        return save_student(usn, student)
    return False


def get_ilm_history(usn: str, subject: str) -> List[Dict[str, Any]]:
    """Get ILM chat history for a student and subject. Returns empty list if not found."""
    path = os.path.join(ILM_HISTORY_PATH, f"{usn}_{subject}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading ILM history {path}: {e}")
    return []


def save_ilm_history(usn: str, subject: str, history: List[Dict[str, Any]]) -> bool:
    """Save ILM chat history for a student and subject. Returns True if successful."""
    path = os.path.join(ILM_HISTORY_PATH, f"{usn}_{subject}.json")
    try:
        with tempfile.NamedTemporaryFile("w", delete=False, dir=ILM_HISTORY_PATH, encoding="utf-8") as tf:
            json.dump(history, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving ILM history {path}: {e}")
        return False


def add_doubt(usn: str, subject: str, doubt: str) -> bool:
    """Add a doubt for a student in a subject. Returns True if successful."""
    student = get_student(usn)
    if student:
        if 'doubts' not in student or not isinstance(student['doubts'], dict):
            student['doubts'] = {}
        if subject not in student['doubts'] or not isinstance(student['doubts'][subject], list):
            student['doubts'][subject] = []
        student['doubts'][subject].append(doubt)
        return save_student(usn, student)
    return False


def get_progress(usn: str) -> Dict[str, Any]:
    """Get student's progress data. Returns empty dict if not found."""
    student = get_student(usn)
    if student:
        return {
            'focus_stats': student.get('focus_stats', {}),
            'marks': student.get('marks', {}),
            'attendance': student.get('attendance', {}),
            'strong_subjects': student.get('strong_subjects', []),
            'weak_subjects': student.get('weak_subjects', []),
            'overall_analysis': student.get('overall_analysis', {})
        }
    return {}


def get_course_contents(usn: str) -> Dict[str, Any]:
    """Get course contents for all enrolled courses. Returns empty dict if not found."""
    student = get_student(usn)
    if student:
        return student.get('course_contents', {})
    return {}


def update_ilm_score(usn: str, subject: str, score: int) -> bool:
    """Update ILM learning rate score and persist. Returns True if successful."""
    return update_learning_rate(usn, score)
    # Optionally, log this update in ILM history or analytics


def get_leaderboard() -> List[Dict[str, Any]]:
    """Return a leaderboard based on learning rate or other gamification metrics."""
    leaderboard = []
    try:
        for fname in os.listdir(DB_PATH):
            if fname.endswith('.json'):
                usn = fname[:-5]
                student = get_student(usn)
                if student:
                    leaderboard.append({
                        'usn': usn,
                        'name': student.get('name', ''),
                        'learning_rate': student.get('learning_rate', 0),
                        'marks': student.get('marks', {})
                    })
        leaderboard.sort(key=lambda x: x['learning_rate'], reverse=True)
    except Exception as e:
        print(f"Error building leaderboard: {e}")
    return leaderboard

### --- Gamification and Insights Functions ---
def get_student_badges(usn: str) -> List[str]:
    """Return a list of badges earned by the student based on progress, marks, and activity."""
    student = get_student(usn)
    badges = []
    if not student:
        return badges
    if student.get('learning_rate', 0) >= 90:
        badges.append('Fast Learner')
    if sum(student.get('marks', {}).values()) > 400:
        badges.append('High Scorer')
    if len(student.get('doubts', {})) > 10:
        badges.append('Curious Mind')
    if student.get('attendance', {}).get('total', 0) > 95:
        badges.append('Attendance Star')
    return badges

def get_subject_difficulty_insights(usn: str) -> Dict[str, Any]:
    """Return insights on subjects/topics where the student faces difficulty."""
    student = get_student(usn)
    insights = {}
    if not student:
        return insights
    weak_subjects = student.get('weak_subjects', [])
    for subject in weak_subjects:
        insights[subject] = {
            'doubts_asked': len(student.get('doubts', {}).get(subject, [])),
            'marks': student.get('marks', {}).get(subject, 0),
            'learning_rate': student.get('learning_rate', 0)
        }
    return insights

def get_recent_activity(usn: str, subject: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Return recent ILM chat history/activity for a student in a subject."""
    history = get_ilm_history(usn, subject)
    return history[-limit:] if history else []

# --- DB Connectivity Helpers ---
def init_db_structure():
    """Ensure all required DB folders exist."""
    os.makedirs(DB_PATH, exist_ok=True)
    os.makedirs(ILM_HISTORY_PATH, exist_ok=True)

def backup_student_db(backup_dir: str) -> bool:
    """Backup all student JSON files to a given directory."""
    try:
        os.makedirs(backup_dir, exist_ok=True)
        for fname in os.listdir(DB_PATH):
            if fname.endswith('.json'):
                src = os.path.join(DB_PATH, fname)
                dst = os.path.join(backup_dir, fname)
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    fdst.write(fsrc.read())
        return True
    except Exception as e:
        print(f"Error backing up student DB: {e}")
        return False

def get_student_llm():
    """Instantiate and return a student LLM client."""
    # Use a generic prompt for student context
    prompt = prompt_ilm_chat_summary(["student session"])
    return create_llm_client(GEMINI_API_KEY, prompt)

def generate_content_with_llm(usn: str, subject: str, user_input: str) -> str:
    """
    Use Gemini LLM to generate course content or assessment for the student.
    Pass prompt, learning rate, and chat history as context.
    """
    llm = get_student_llm()
    learning_rate = get_learning_rate(usn)
    chat_history = get_ilm_history(usn, subject)
    summary = prompt_ilm_chat_summary(chat_history)
    prompt = prompt_student_content(subject, learning_rate, summary)
    response = llm.generate_response(prompt, user_input)
    return response

def solve_doubt_with_llm(usn: str, subject: str, doubt: str) -> str:
    """
    Use Gemini LLM to solve a student's doubt, update chat history and learning rate.
    """
    llm = get_student_llm()
    chat_history = get_ilm_history(usn, subject)
    summary = prompt_ilm_chat_summary(chat_history)
    prompt = prompt_student_doubt_solving(subject, doubt, summary)
    response = llm.generate_response(prompt, "")
    chat_history.append({"role": "student", "message": doubt})
    chat_history.append({"role": "ilm", "message": response})
    save_ilm_history(usn, subject, chat_history)
    learning_rate = get_learning_rate(usn)
    update_learning_rate(usn, min(100, learning_rate + 2))
    return response


def generate_insight_with_llm(usn: str, subject: str) -> str:
    """
    Use Gemini LLM to generate insights for a student in a subject.
    """
    llm = get_student_llm()
    performance_data = get_progress(usn)
    prompt = prompt_student_insights(subject, performance_data)
    response = llm.generate_response(prompt, "")
    return response

def generate_assessment_with_llm(usn: str, subject: str) -> str:
    """
    Use Gemini LLM to generate a personalized assessment/quiz for the student in a subject.
    Difficulty and length adapt to learning rate.
    """
    llm = get_student_llm()
    learning_rate = get_learning_rate(usn)
    chat_history = get_ilm_history(usn, subject)
    summary = prompt_ilm_chat_summary(chat_history)
    prompt = prompt_student_assessment(subject, learning_rate, summary)
    response = llm.generate_response(prompt, "")
    return response


def generate_gamification_feedback_with_llm(usn: str) -> str:
    """
    Use Gemini LLM to generate gamified feedback, challenges, and leaderboard insights for the student.
    """
    llm = get_student_llm()
    progress = get_progress(usn)
    prompt = prompt_student_gamification("all", progress)
    response = llm.generate_response(prompt, "")
    return response


def generate_teacher_insight_with_llm(usn: str, subject: str) -> str:
    """
    Use Gemini LLM to generate insights for the teacher about student difficulties in a subject/topic.
    """
    llm = get_student_llm()
    chat_history = get_ilm_history(usn, subject)
    summary = prompt_ilm_chat_summary(chat_history)
    prompt = prompt_student_teacher_insights(subject, summary)
    response = llm.generate_response(prompt, "")
    return response


def generate_and_store_login_context(usn: str):
    """
    On student login, generate and store ILM chat history summary for each enrolled course using LLM.
    Summary is based on last 5 messages and stored for session context.
    """
    student = get_student(usn)
    if not student:
        return False
    enrolled_courses = student.get('enrolled_courses', [])
    llm_client = get_student_llm()
    learning_rate = get_learning_rate(usn)
    context_summaries = {}
    for subject in enrolled_courses:
        chat_history = get_ilm_history(usn, subject)
        last_msgs = [h['message'] for h in chat_history[-5:]] if chat_history else []
        prompt = prompt_ilm_chat_summary(last_msgs)
        summary = llm_client.generate_response(prompt, "")
        # Store summary and learning rate for session
        context_summaries[subject] = {
            "summary": summary,
            "learning_rate": learning_rate
        }
        # Optionally, persist to file for session context
        session_path = os.path.join(DB_PATH, f"{usn}_{subject}_session.json")
        with open(session_path, "w", encoding="utf-8") as f:
            json.dump(context_summaries[subject], f, indent=2)
    return True