from fastapi import APIRouter, HTTPException
from app.repo.parent_repo import (
    generate_behavioral_analysis_with_llm,
    generate_doubt_frequency_insight_with_llm,
    communicate_with_teacher_llm
)

router = APIRouter()

@router.post("/parent/{parent_id}/behavioral_analysis/{child_usn}")
def behavioral_analysis(parent_id: str, child_usn: str):
    return {"response": generate_behavioral_analysis_with_llm(child_usn)}

@router.post("/parent/{parent_id}/doubt_frequency/{child_usn}")
def doubt_frequency(parent_id: str, child_usn: str):
    return {"response": generate_doubt_frequency_insight_with_llm(child_usn)}

@router.post("/parent/{parent_id}/communicate/{teacher_id}/{child_usn}")
def communicate_teacher(parent_id: str, teacher_id: str, child_usn: str, message: str):
    return {"response": communicate_with_teacher_llm(parent_id, teacher_id, child_usn, message)}
