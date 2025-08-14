from fastapi import APIRouter, HTTPException
from app.repo.teacher_repo import (
    generate_attendance_insight_with_llm,
    generate_content_with_llm_for_teacher,
    generate_assignment_with_llm,
    evaluate_student_with_llm,
    communicate_with_class_llm,
    communicate_with_student_llm
)

router = APIRouter()

@router.post("/teacher/{teacher_id}/attendance_insight/{course}")
def attendance_insight(teacher_id: str, course: str):
    return {"response": generate_attendance_insight_with_llm(teacher_id, course)}

@router.post("/teacher/{teacher_id}/content/{course}")
def content_generation(teacher_id: str, course: str, topic: str):
    return {"response": generate_content_with_llm_for_teacher(teacher_id, course, topic)}

@router.post("/teacher/{teacher_id}/assignment/{course}")
def assignment_generation(teacher_id: str, course: str, topic: str):
    return {"response": generate_assignment_with_llm(teacher_id, course, topic)}

@router.post("/teacher/{teacher_id}/evaluate/{course}/{student_usn}")
def evaluate_submission(teacher_id: str, course: str, student_usn: str, submission: str):
    return {"response": evaluate_student_with_llm(teacher_id, course, student_usn, submission)}

@router.post("/teacher/{teacher_id}/communicate/class/{course}")
def communicate_class(teacher_id: str, course: str, message: str):
    return {"response": communicate_with_class_llm(teacher_id, course, message)}

@router.post("/teacher/{teacher_id}/communicate/student/{course}/{student_usn}")
def communicate_student(teacher_id: str, course: str, student_usn: str, message: str):
    return {"response": communicate_with_student_llm(teacher_id, course, student_usn, message)}
