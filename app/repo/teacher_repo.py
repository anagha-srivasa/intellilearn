import os
import json
from typing import Any, Dict, List, Optional
import tempfile
import yaml
from llm import llm_client
from resources.prompts import (
    prompt_teacher_attendance_insights,
    prompt_teacher_content_generation,
    prompt_teacher_assignment_generation,
    prompt_teacher_evaluation,
    prompt_teacher_communication,
    prompt_ilm_chat_summary
)

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'teachers')
ILM_HISTORY_PATH = os.path.join(PROJECT_ROOT, 'db', 'ilm_history')
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'config.yml')

with open(CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f)
GEMINI_API_KEY = config['llm']['gemini_api_key']

os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(ILM_HISTORY_PATH, exist_ok=True)

# --- Teacher Data Access ---
def get_teacher(teacher_id: str) -> Optional[Dict[str, Any]]:
    path = os.path.join(DB_PATH, f"{teacher_id}.json")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Error reading teacher file {path}: {e}")
    return None


def save_teacher(teacher_id: str, data: Dict[str, Any]) -> bool:
    path = os.path.join(DB_PATH, f"{teacher_id}.json")
    try:
        with tempfile.NamedTemporaryFile("w", delete=False, dir=DB_PATH, encoding="utf-8") as tf:
            json.dump(data, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving teacher file {path}: {e}")
        return False

# --- Attendance Insights ---
def get_attendance_reports(teacher_id: str) -> Dict[str, Any]:
    teacher = get_teacher(teacher_id)
    return teacher.get('attendance_reports', {}) if teacher else {}


def get_attendance_outliers(teacher_id: str, threshold: int = 80) -> Dict[str, List[str]]:
    """Return students with attendance below threshold for each course."""
    teacher = get_teacher(teacher_id)
    outliers = {}
    if teacher:
        for course, students in teacher.get('attendance_reports', {}).items():
            outliers[course] = [usn for usn, att in students.items() if att < threshold]
    return outliers


def get_attendance_anomalies(teacher_id: str) -> Dict[str, List[str]]:
    """Detect anomalies in attendance pattern (simple: large drop vs previous)."""
    teacher = get_teacher(teacher_id)
    anomalies = {}
    if teacher:
        for course, students in teacher.get('attendance_reports', {}).items():
            anomalies[course] = [usn for usn, att in students.items() if att < 50]  # Example rule
    return anomalies

# --- Course & Student Management ---
def get_courses(teacher_id: str) -> List[str]:
    teacher = get_teacher(teacher_id)
    return teacher.get('courses', []) if teacher else []


def get_students_in_course(teacher_id: str, course: str) -> List[str]:
    teacher = get_teacher(teacher_id)
    return teacher.get('students', {}).get(course, []) if teacher else []


def get_student_performance(teacher_id: str, course: str) -> Dict[str, Any]:
    teacher = get_teacher(teacher_id)
    return teacher.get('performance', {}).get(course, {}) if teacher else {}

# --- Learning Rate & Topics ---
def get_student_learning_rates(teacher_id: str, course: str) -> Dict[str, int]:
    teacher = get_teacher(teacher_id)
    # This would typically be fetched from student repo, here just a placeholder
    return {usn: 0 for usn in teacher.get('students', {}).get(course, [])} if teacher else {}


def get_topics_to_stress(teacher_id: str) -> Dict[str, List[str]]:
    teacher = get_teacher(teacher_id)
    return teacher.get('topics_to_stress', {}) if teacher else {}

# --- Content Approval & Delivery ---
def get_approved_contents(teacher_id: str, course: str) -> List[str]:
    teacher = get_teacher(teacher_id)
    return teacher.get('approved_contents', {}).get(course, []) if teacher else []


def approve_content(teacher_id: str, course: str, content: str) -> bool:
    teacher = get_teacher(teacher_id)
    if teacher:
        if 'approved_contents' not in teacher:
            teacher['approved_contents'] = {}
        if course not in teacher['approved_contents']:
            teacher['approved_contents'][course] = []
        if content not in teacher['approved_contents'][course]:
            teacher['approved_contents'][course].append(content)
        return save_teacher(teacher_id, teacher)
    return False

# --- Assignment Management ---
def get_personal_assignments(teacher_id: str, course: str) -> List[str]:
    teacher = get_teacher(teacher_id)
    return teacher.get('personal_assignments', {}).get(course, []) if teacher else []


def add_personal_assignment(teacher_id: str, course: str, assignment: str) -> bool:
    teacher = get_teacher(teacher_id)
    if teacher:
        if 'personal_assignments' not in teacher:
            teacher['personal_assignments'] = {}
        if course not in teacher['personal_assignments']:
            teacher['personal_assignments'][course] = []
        if assignment not in teacher['personal_assignments'][course]:
            teacher['personal_assignments'][course].append(assignment)
        return save_teacher(teacher_id, teacher)
    return False

# --- Evaluation Modes ---
def get_evaluation_mode(teacher_id: str, course: str) -> str:
    teacher = get_teacher(teacher_id)
    return teacher.get('evaluation_mode', {}).get(course, 'manual') if teacher else 'manual'


def set_evaluation_mode(teacher_id: str, course: str, mode: str) -> bool:
    teacher = get_teacher(teacher_id)
    if teacher:
        if 'evaluation_mode' not in teacher:
            teacher['evaluation_mode'] = {}
        teacher['evaluation_mode'][course] = mode
        return save_teacher(teacher_id, teacher)
    return False

# --- Communication ---
def add_teacher_message(teacher_id: str, course: str, message: str, to_class: bool = True, student_usn: Optional[str] = None) -> bool:
    """Add a message from teacher to class or specific student."""
    history_file = f"{teacher_id}_{course}.json" if to_class else f"{teacher_id}_{course}_{student_usn}.json"
    path = os.path.join(ILM_HISTORY_PATH, history_file)
    try:
        history = []
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                history = json.load(f)
        history.append({"role": "teacher", "message": message})
        with tempfile.NamedTemporaryFile("w", delete=False, dir=ILM_HISTORY_PATH, encoding="utf-8") as tf:
            json.dump(history, tf, indent=2)
            tempname = tf.name
        os.replace(tempname, path)
        return True
    except Exception as e:
        print(f"Error saving teacher message {path}: {e}")
        return False


# --- Analytics and Insights Functions ---
def get_course_performance_summary(teacher_id: str, course: str) -> Dict[str, Any]:
    """Return summary statistics for student performance in a course."""
    performance = get_student_performance(teacher_id, course)
    if not performance:
        return {}
    scores = list(performance.values())
    return {
        "average": sum(scores) / len(scores) if scores else 0,
        "max": max(scores) if scores else 0,
        "min": min(scores) if scores else 0,
        "count": len(scores)
    }

def get_student_improvement_suggestions(teacher_id: str, course: str) -> Dict[str, str]:
    """Suggest improvement areas for students based on performance and attendance."""
    performance = get_student_performance(teacher_id, course)
    attendance = get_attendance_reports(teacher_id).get(course, {})
    suggestions = {}
    for usn, score in performance.items():
        att = attendance.get(usn, 100)
        if score < 50:
            suggestions[usn] = "Needs improvement in scoring."
        elif att < 75:
            suggestions[usn] = "Needs better attendance."
        else:
            suggestions[usn] = "Good performance."
    return suggestions

def get_teacher_activity_log(teacher_id: str) -> List[Dict[str, Any]]:
    """Return a log of teacher's recent messages to classes and students."""
    logs = []
    for fname in os.listdir(ILM_HISTORY_PATH):
        if fname.startswith(teacher_id + "_") and fname.endswith('.json'):
            path = os.path.join(ILM_HISTORY_PATH, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    history = json.load(f)
                    for entry in history:
                        if entry.get("role") == "teacher":
                            logs.append({"file": fname, "message": entry.get("message")})
            except Exception as e:
                print(f"Error reading activity log {path}: {e}")
    return logs

def get_course_engagement_stats(teacher_id: str, course: str) -> Dict[str, Any]:
    """Return engagement stats for a course (messages, assignments, content approvals)."""
    teacher = get_teacher(teacher_id)
    stats = {}
    if not teacher:
        return stats
    # Count messages
    msg_file = f"{teacher_id}_{course}.json"
    msg_path = os.path.join(ILM_HISTORY_PATH, msg_file)
    msg_count = 0
    if os.path.exists(msg_path):
        try:
            with open(msg_path, "r", encoding="utf-8") as f:
                msg_count = len(json.load(f))
        except Exception as e:
            print(f"Error reading messages for engagement stats: {e}")
    stats["messages"] = msg_count
    # Assignments
    stats["assignments"] = len(get_personal_assignments(teacher_id, course))
    # Content approvals
    stats["approved_contents"] = len(get_approved_contents(teacher_id, course))
    return stats

def get_llm_client():
    from resources.prompts import prompt_ilm_chat_summary
    from llm.llm_client import create_llm_client
    prompt = prompt_ilm_chat_summary(["teacher session"])
    return create_llm_client(GEMINI_API_KEY, prompt)

def generate_attendance_insight_with_llm(teacher_id: str, course: str) -> str:
    """
    Use Gemini LLM to generate AI insights on attendance outliers and anomalies for a course.
    """
    llm = get_llm_client()
    attendance_data = {
        "outliers": get_attendance_outliers(teacher_id).get(course, []),
        "anomalies": get_attendance_anomalies(teacher_id).get(course, [])
    }
    prompt = prompt_teacher_attendance_insights(attendance_data)
    return llm.generate_response(prompt, "")


def generate_content_with_llm_for_teacher(teacher_id: str, course: str, topic: str) -> str:
    """
    Use Gemini LLM to generate course content for a topic, for teacher approval.
    """
    llm = get_llm_client()
    # For teacher, we can use a generic learning rate and summary (could be extended)
    learning_rate = 50
    summary = prompt_ilm_chat_summary([topic])
    prompt = prompt_teacher_content_generation(course, learning_rate, summary)
    return llm.generate_response(prompt, "")


def generate_assignment_with_llm(teacher_id: str, course: str, topic: str) -> str:
    """
    Use Gemini LLM to generate a tailor-made assignment or question set for a topic.
    """
    llm = get_llm_client()
    learning_rate = 50
    summary = prompt_ilm_chat_summary([topic])
    prompt = prompt_teacher_assignment_generation(course, learning_rate, summary)
    return llm.generate_response(prompt, "")


def evaluate_student_with_llm(teacher_id: str, course: str, student_usn: str, submission: str) -> str:
    """
    Use Gemini LLM to evaluate a student's submission (if in ILM mode).
    """
    llm = get_llm_client()
    mode = get_evaluation_mode(teacher_id, course)
    if mode != "ilm":
        return "Manual evaluation required."
    prompt = prompt_teacher_evaluation(submission)
    return llm.generate_response(prompt, "")


def communicate_with_class_llm(teacher_id: str, course: str, message: str) -> str:
    """
    Use Gemini LLM to enhance teacher-class communication (e.g., announcements, feedback).
    """
    llm = get_llm_client()
    student_summary = prompt_ilm_chat_summary([message])
    prompt = prompt_teacher_communication(message, student_summary)
    return llm.generate_response(prompt, "")


def communicate_with_student_llm(teacher_id: str, course: str, student_usn: str, message: str) -> str:
    """
    Use Gemini LLM to enhance teacher-student communication (e.g., feedback, encouragement).
    """
    llm = get_llm_client()
    student_summary = prompt_ilm_chat_summary([message])
    prompt = prompt_teacher_communication(message, student_summary)
    return llm.generate_response(prompt, "")
