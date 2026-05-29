"""
teacher.py — teacher-only endpoints (JWT + role guard)

AI Summary uses Google Gemini (free tier).
Install: pip install google-generativeai
Set env var: GEMINI_API_KEY=your_key_here
"""
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from dotenv import load_dotenv

from database import SessionLocal
from models import Assignment, Submission, User
from schemas import AssignmentCreate
from security import get_db, require_teacher, get_current_user

router = APIRouter()

load_dotenv()  # loads .env file

# print("API KEY:", os.getenv("GEMINI_API_KEY"))


# ── Suspicion score helper ────────────────────────────────────────────────────

def compute_suspicion(sub: Submission) -> dict:
    """
    Score 0–5 based on typing behaviour signals.
    Higher = more suspicious indicators (NOT a definitive AI claim).
    """
    score = 0
    reasons = []

    if (sub.avg_typing_speed or 0) > 8:       # > 8 chars/sec is unusually fast
        score += 1
        reasons.append("High typing speed")

    total = (sub.typed_count or 0) + (sub.pasted_count or 0)
    if total > 50 and (sub.backspace_count or 0) < 3:
        score += 1
        reasons.append("Very few backspaces")

    if (sub.typing_variance or 0) < 0.05:     # near-constant intervals
        score += 1
        reasons.append("Low typing variability")

    if (sub.burst_events or 0) >= 3:
        score += 1
        reasons.append("Multiple burst insertions")

    if total > 100 and (sub.pause_count or 0) < 2:
        score += 1
        reasons.append("Virtually no pauses")

    if score <= 1:
        level, color = "Normal", "green"
    elif score <= 3:
        level, color = "Mildly Suspicious", "amber"
    else:
        level, color = "Highly Suspicious", "red"

    return {"score": score, "level": level, "color": color, "reasons": reasons}


# ── AI Summary via Gemini ─────────────────────────────────────────────────────

def call_gemini(prompt: str) -> dict:
    """Call Gemini 1.5 Flash (free tier). Falls back gracefully if key missing."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        return {
            "summary"    : "AI summary unavailable — set the GEMINI_API_KEY environment variable.",
            "key_points" : [],
        }
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Parse the model's plain-text response into summary + key_points
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        summary    = lines[0] if lines else text
        key_points = [l.lstrip("-•* ") for l in lines[1:] if l.startswith(("-", "•", "*"))]
        return {"summary": summary, "key_points": key_points}
    except Exception as e:
        return {"summary": f"AI summary error: {str(e)}", "key_points": []}


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/assignments")
def create_assignment(
    assignment   : AssignmentCreate,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(require_teacher),   # ← teachers only
):
    new_assignment = Assignment(
        title       = assignment.title,
        description = assignment.description,
        deadline    = str(assignment.deadline),
        max_marks   = assignment.max_marks,
        teacher_id  = assignment.teacher_id,
        class_id    = assignment.class_id,
    )
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Assignment created", "assignment_id": new_assignment.id}


@router.get("/assignments")
def get_assignments(
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_current_user),
):
    return db.query(Assignment).all()


@router.get("/assignments/class/{class_id}")
def get_assignments_for_class(
    class_id     : str,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_current_user),
):
    return db.query(Assignment).filter(Assignment.class_id == class_id).all()


@router.get("/analytics/{assignment_id}")
def get_analytics(
    assignment_id : int,
    db            : Session = Depends(get_db),
    current_user  : User    = Depends(require_teacher),
):
    submissions = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).all()

    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")

    result = []
    for sub in submissions:
        total      = (sub.typed_count or 0) + (sub.pasted_count or 0)
        typed_pct  = round((sub.typed_count  / total) * 100, 1) if total else 0
        pasted_pct = round((sub.pasted_count / total) * 100, 1) if total else 0

        student      = db.query(User).filter(User.id == sub.student_id).first()
        student_name = student.username if student else f"Student #{sub.student_id}"

        suspicion = compute_suspicion(sub)

        result.append({
            "submission_id"    : sub.id,
            "student_id"       : sub.student_id,
            "student_name"     : student_name,
            "content"          : sub.content,
            "typed_%"          : typed_pct,
            "pasted_%"         : pasted_pct,
            "marks"            : sub.marks,
            # typing behaviour
            "avg_typing_speed" : round(sub.avg_typing_speed or 0, 2),
            "typing_variance"  : round(sub.typing_variance  or 0, 3),
            "pause_count"      : sub.pause_count      or 0,
            "backspace_count"  : sub.backspace_count  or 0,
            "burst_events"     : sub.burst_events     or 0,
            # suspicion
            "suspicion_score"  : suspicion["score"],
            "suspicion_level"  : suspicion["level"],
            "suspicion_color"  : suspicion["color"],
            "suspicion_reasons": suspicion["reasons"],
        })

    return result


@router.patch("/submissions/{submission_id}/marks")
def update_marks(
    submission_id : int,
    body          : dict,
    db            : Session = Depends(get_db),
    current_user  : User    = Depends(require_teacher),
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    sub.marks = body.get("marks", sub.marks)
    db.commit()
    return {"message": "Marks updated"}


@router.get("/summarize-submission/{submission_id}")
def summarize_submission(
    submission_id : int,
    db            : Session = Depends(get_db),
    current_user  : User    = Depends(require_teacher),
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    student      = db.query(User).filter(User.id == sub.student_id).first()
    student_name = student.username if student else f"Student #{sub.student_id}"

    prompt = (
        f"You are an academic assistant. A student named '{student_name}' submitted the following assignment.\n\n"
        f"---\n{sub.content}\n---\n\n"
        f"Please provide:\n"
        f"1. A concise 3-5 line summary of the submission.\n"
        f"2. Up to 5 key points as bullet points starting with '-'.\n\n"
        f"Do not invent information. Base your response only on the text above."
    )
    return call_gemini(prompt)


# Legacy bulk summarize (kept for compatibility)
@router.get("/summarize/{assignment_id}")
def summarize(
    assignment_id : int,
    db            : Session = Depends(get_db),
    current_user  : User    = Depends(require_teacher),
):
    submissions = db.query(Submission).filter(
        Submission.assignment_id == assignment_id
    ).all()
    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")

    combined = "\n---\n".join([s.content for s in submissions])
    prompt   = (
        f"Summarise the following {len(submissions)} student submissions in 4-6 lines, "
        f"noting common themes and any outliers:\n\n{combined[:3000]}"
    )
    return call_gemini(prompt)