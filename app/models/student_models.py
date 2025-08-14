from pydantic import BaseModel
from typing import List, Dict, Any

# Placeholder for student models

class Student(BaseModel):
    usn: str
    name: str
    enrolled_courses: List[str]
    learning_rate: int
    marks: Dict[str, int]
    attendance: Dict[str, Any]
    doubts: Dict[str, List[str]]
    strong_subjects: List[str]
    weak_subjects: List[str]
    overall_analysis: Dict[str, Any]
    course_contents: Dict[str, List[str]]
