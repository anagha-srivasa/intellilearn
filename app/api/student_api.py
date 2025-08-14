from fastapi import APIRouter, HTTPException
from app.repo.student_repo import (
    generate_and_store_login_context,
    generate_content_with_llm,
    solve_doubt_with_llm,
    generate_assessment_with_llm,
    generate_insight_with_llm,
    generate_gamification_feedback_with_llm,
    generate_teacher_insight_with_llm
)

router = APIRouter()
@router.post("/student/login/{usn}")
def student_login(usn: str):
    success = generate_and_store_login_context(usn)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Login context generated"}

@router.post("/student/{usn}/content/{subject}")
def get_content(usn: str, subject: str, user_input: str):
    return {"response": generate_content_with_llm(usn, subject, user_input)}

@router.post("/student/{usn}/doubt/{subject}")
def solve_doubt(usn: str, subject: str, doubt: str):
    return {"response": solve_doubt_with_llm(usn, subject, doubt)}

@router.post("/student/{usn}/assessment/{subject}")
def get_assessment(usn: str, subject: str):
    return {"response": generate_assessment_with_llm(usn, subject)}

@router.post("/student/{usn}/insight/{subject}")
def get_insight(usn: str, subject: str):
    return {"response": generate_insight_with_llm(usn, subject)}

@router.post("/student/{usn}/gamification")
def get_gamification(usn: str):
    return {"response": generate_gamification_feedback_with_llm(usn)}

@router.post("/student/{usn}/teacher_insight/{subject}")
def get_teacher_insight(usn: str, subject: str):
    return {"response": generate_teacher_insight_with_llm(usn, subject)}
