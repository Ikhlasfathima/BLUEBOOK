"""
student.py — submission endpoints (JWT-protected, role-guarded)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models import Submission, Assignment, User
from schemas import SubmissionCreate
from security import get_db, require_student, get_current_user

router = APIRouter()


@router.post("/submit")
def submit_assignment(
    submission : SubmissionCreate,
    db         : Session = Depends(get_db),
    current_user: User   = Depends(require_student),   # ← students only
):
    # Verify assignment exists
    assignment = db.query(Assignment).filter(
        Assignment.id == submission.assignment_id
    ).first()
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    # Deadline enforcement
    if assignment.deadline:
        try:
            deadline_date = date.fromisoformat(str(assignment.deadline))
            if date.today() > deadline_date:
                raise HTTPException(
                    status_code=400,
                    detail=f"Submission deadline has passed ({assignment.deadline})"
                )
        except ValueError:
            pass

    new_submission = Submission(
        student_id       = submission.student_id,
        assignment_id    = submission.assignment_id,
        content          = submission.content,
        typed_count      = submission.typed_count,
        pasted_count     = submission.pasted_count,
        avg_typing_speed = submission.avg_typing_speed,
        typing_variance  = submission.typing_variance,
        pause_count      = submission.pause_count,
        backspace_count  = submission.backspace_count,
        burst_events     = submission.burst_events,
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)
    return {"message": "Submitted successfully", "submission_id": new_submission.id}


@router.get("/submissions/{student_id}")
def get_student_submissions(
    student_id   : int,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_current_user),
):
    return db.query(Submission).filter(Submission.student_id == student_id).all()


@router.get("/my-submissions/{student_id}")
def get_my_submissions(
    student_id   : int,
    db           : Session = Depends(get_db),
    current_user : User    = Depends(get_current_user),
):
    subs = db.query(Submission).filter(Submission.student_id == student_id).all()

    result = []
    for sub in subs:
        assignment = db.query(Assignment).filter(Assignment.id == sub.assignment_id).first()
        result.append({
            "submission_id"    : sub.id,
            "assignment_id"    : sub.assignment_id,
            "assignment_title" : assignment.title if assignment else f"Assignment #{sub.assignment_id}",
            "content"          : sub.content,
            "marks"            : sub.marks,
            "max_marks"        : assignment.max_marks if assignment else None,
        })
    return result