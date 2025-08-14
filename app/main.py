from fastapi import FastAPI
from app.api.student_api import router as student_router
from app.api.teacher_api import router as teacher_router
from app.api.parent_api import router as parent_router

app = FastAPI()

# Include routers for all user types
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(parent_router)

# --- Frontend ---
# Run Streamlit dashboards separately:
#   streamlit run dashboard/student_dashboard.py
#   streamlit run dashboard/teacher_dashboard.py
#   streamlit run dashboard/parent_dashboard.py
