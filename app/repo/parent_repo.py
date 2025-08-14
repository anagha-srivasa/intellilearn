import os
import json
from typing import Any, Dict, List, Optional
import tempfile
import yaml
from llm import llm_client
from resources.prompts import (
    prompt_parent_behavioral_analysis,
    prompt_parent_doubt_frequency,
    prompt_parent_teacher_communication,
    prompt_ilm_chat_summary
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'parents')
STUDENT_DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'students')
ILM_HISTORY_PATH = os.path.join(PROJECT_ROOT, 'db', 'ilm_history')
TEACHER_DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'teachers')
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.yml')

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)
GEMINI_API_KEY = config['llm']['gemini_api_key']

os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(ILM_HISTORY_PATH, exist_ok=True)

# --- Parent Data Access ---
def get_parent(parent_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(DB_PATH, f"{parent_id}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading parent file {path}: {e}")
    return None


def save_parent(parent_id: str, data: Dict[str, Any]) -> bool:
    path = os.path.join(DB_PATH, f"{parent_id}.json")
    try:
        with tempfile.NamedTemporaryFile("w", delete=False, dir=DB_PATH, encoding="utf-8") as tf:
            json.dump(data, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving parent file {path}: {e}")
        return False

# --- Student Monitoring ---
def get_children(parent_id: str) -> List[str]:
    parent = get_parent(parent_id)
    return parent.get('children', []) if parent else []


def get_child_data(child_usn: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(STUDENT_DB_PATH, f"{child_usn}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading child file {path}: {e}")
    return None


def get_scoring_pattern(child_usn: str) -> Dict[str, Any]:
    child = get_child_data(child_usn)
    return child.get('marks', {}) if child else {}


def get_attendance(child_usn: str) -> Dict[str, Any]:
    child = get_child_data(child_usn)
    return child.get('attendance', {}) if child else {}


def get_doubt_frequency(child_usn: str) -> Dict[str, int]:
    child = get_child_data(child_usn)
    freq = {}
    if child and 'doubts' in child:
        for subject, doubts in child['doubts'].items():
            freq[subject] = len(doubts)
    return freq


def get_interaction_analysis(child_usn: str) -> Dict[str, Any]:
    child = get_child_data(child_usn)
    analysis = {}
    if child:
        analysis['doubt_frequency'] = get_doubt_frequency(child_usn)
        analysis['learning_rate'] = child.get('learning_rate', 0)
        analysis['focus_stats'] = child.get('focus_stats', {})
        analysis['overall_analysis'] = child.get('overall_analysis', {})
    return analysis


def get_chat_history_summary(child_usn: str, subject: str, limit: int = 5) -> str:
    path = os.path.join(ILM_HISTORY_PATH, f"{child_usn}_{subject}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
                messages = [h['message'] for h in history[-limit:]]
                return " | ".join(messages)
    except Exception as e:
        print(f"Error reading chat history {path}: {e}")
    return ""

# --- Parent-Teacher Communication ---
def get_teachers_for_child(child_usn: str) -> List[str]:
    teachers = []
    for fname in os.listdir(TEACHER_DB_PATH):
        if fname.endswith('.json'):
            path = os.path.join(TEACHER_DB_PATH, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    teacher = json.load(f)
                    for course, students in teacher.get('students', {}).items():
                        if child_usn in students:
                            teachers.append(teacher.get('teacher_id', ''))
            except Exception as e:
                print(f"Error reading teacher file {path}: {e}")
    return teachers


def add_parent_teacher_message(parent_id: str, teacher_id: str, child_usn: str, message: str) -> bool:
    """Add a message from parent to teacher regarding a child."""
    history_file = f"{parent_id}_{teacher_id}_{child_usn}.json"
    path = os.path.join(ILM_HISTORY_PATH, history_file)
    try:
        history = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append({"role": "parent", "message": message})
        with tempfile.NamedTemporaryFile("w", delete=False, dir=ILM_HISTORY_PATH, encoding="utf-8") as tf:
            json.dump(history, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving parent-teacher message {path}: {e}")
        return False


# --- Behavioral Analysis and Reporting Functions ---
def get_child_behavioral_summary(child_usn: str) -> Dict[str, Any]:
    """Return a summary of behavioral patterns for a child."""
    child = get_child_data(child_usn)
    if not child:
        return {}
    summary = {
        "learning_rate": child.get("learning_rate", 0),
        "focus_stats": child.get("focus_stats", {}),
        "doubt_frequency": get_doubt_frequency(child_usn),
        "attendance": child.get("attendance", {}),
        "marks": child.get("marks", {}),
        "strong_subjects": child.get("strong_subjects", []),
        "weak_subjects": child.get("weak_subjects", []),
        "overall_analysis": child.get("overall_analysis", {})
    }
    return summary

def get_child_doubt_trend(child_usn: str, subject: str) -> List[int]:
    """Return a trend of doubt counts over time for a subject."""
    path = os.path.join(ILM_HISTORY_PATH, f"{child_usn}_{subject}.json")
    trend = []
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
                for entry in history:
                    if entry.get("role") == "student":
                        trend.append(1)
        # Cumulative trend (e.g., [1,2,3,...])
        for i in range(1, len(trend)):
            trend[i] += trend[i-1]
    except Exception as e:
        print(f"Error reading doubt trend {path}: {e}")
    return trend

def get_child_login_history(child_usn: str) -> List[str]:
    """Return a list of login timestamps for a child (stub, extend as needed)."""
    # This would require a login tracking mechanism; here is a stub
    return []

def get_parent_report_for_child(parent_id: str, child_usn: str) -> Dict[str, Any]:
    """Generate a comprehensive report for a child for the parent."""
    report = {
        "behavioral_summary": get_child_behavioral_summary(child_usn),
        "doubt_trend": {subject: get_child_doubt_trend(child_usn, subject) for subject in get_doubt_frequency(child_usn).keys()},
        "chat_history_summaries": {subject: get_chat_history_summary(child_usn, subject) for subject in get_doubt_frequency(child_usn).keys()},
        "teachers": get_teachers_for_child(child_usn)
    }
    return report

def get_parent_llm():
    """Instantiate and return a parent LLM client."""
    from resources.prompts import prompt_ilm_chat_summary
    from llm.llm_client import create_llm_client
    prompt = prompt_ilm_chat_summary(["parent session"])
    return create_llm_client(GEMINI_API_KEY, prompt)

def generate_behavioral_analysis_with_llm(child_usn: str) -> str:
    """
    Use Gemini LLM to generate behavioral analysis for a child based on scoring, attendance, doubts, and interaction.
    """
    llm = get_parent_llm()
    student_data = get_child_data(child_usn)
    prompt = prompt_parent_behavioral_analysis(student_data)
    return llm.generate_response(prompt, "")


def generate_doubt_frequency_insight_with_llm(child_usn: str) -> str:
    """
    Use Gemini LLM to analyze doubt frequency and interaction for a child.
    """
    llm = get_parent_llm()
    doubt_data = get_doubt_frequency(child_usn)
    prompt = prompt_parent_doubt_frequency(doubt_data)
    return llm.generate_response(prompt, "")


def communicate_with_teacher_llm(parent_id: str, teacher_id: str, child_usn: str, message: str) -> str:
    """
    Use Gemini LLM to enhance parent-teacher communication regarding a child.
    """
    llm = get_parent_llm()
    teacher_summary = prompt_ilm_chat_summary([message])
    prompt = prompt_parent_teacher_communication(message, teacher_summary)
    return llm.generate_response(prompt, "")
