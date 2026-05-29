from pydantic import BaseModel, Field, EmailStr
from datetime import date
from enum import Enum
from typing import Optional


class RoleEnum(str, Enum):
    teacher = "teacher"
    student = "student"


# ── Auth ──────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    username : str      = Field(min_length=3, max_length=50)
    email    : EmailStr
    password : str      = Field(min_length=4)
    role     : RoleEnum
    class_id : Optional[str] = None


class LoginRequest(BaseModel):
    username : str
    password : str


# ── Assignments ───────────────────────────────────────────────────────────────

class AssignmentCreate(BaseModel):
    title       : str           = Field(min_length=3, max_length=100)
    description : str           = ""
    deadline    : date                         # YYYY-MM-DD
    max_marks   : int           = Field(gt=0, le=1000)
    teacher_id  : int
    class_id    : Optional[str] = None
    # NOTE: deadline validator removed — caused 422 errors due to Windows timezone issues


# ── Submissions ───────────────────────────────────────────────────────────────

class SubmissionCreate(BaseModel):
    student_id    : int
    assignment_id : int
    content       : str   = Field(min_length=1)   # relaxed — HTML content can be brief

    # paste tracking
    typed_count   : int   = 0
    pasted_count  : int   = 0

    # typing behaviour analytics
    avg_typing_speed : float = 0.0
    typing_variance  : float = 0.0
    pause_count      : int   = 0
    backspace_count  : int   = 0
    burst_events     : int   = 0