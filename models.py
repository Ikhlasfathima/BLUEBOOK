from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class User(Base):
    __tablename__ = "users"

    id       = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email    = Column(String, unique=True)
    password = Column(String)           # bcrypt hashed
    role     = Column(String)
    class_id = Column(String, nullable=True)   # e.g. "3rd Year BCA" — students only


class Assignment(Base):
    __tablename__ = "assignments"

    id          = Column(Integer, primary_key=True, index=True)
    title       = Column(String)
    description = Column(String)
    deadline    = Column(String)        # stored as YYYY-MM-DD string
    max_marks   = Column(Integer)
    teacher_id  = Column(Integer, ForeignKey("users.id"))
    class_id    = Column(String, nullable=True)   # which class this targets


class Submission(Base):
    __tablename__ = "submissions"

    id            = Column(Integer, primary_key=True, index=True)
    student_id    = Column(Integer, ForeignKey("users.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    content       = Column(String)

    # paste tracking (original)
    typed_count   = Column(Integer, default=0)
    pasted_count  = Column(Integer, default=0)

    # typing behaviour analytics (new)
    avg_typing_speed = Column(Float,   default=0.0)   # chars per second
    typing_variance  = Column(Float,   default=0.0)   # std-dev of inter-key intervals
    pause_count      = Column(Integer, default=0)     # pauses > 2 s
    backspace_count  = Column(Integer, default=0)
    burst_events     = Column(Integer, default=0)     # large inserts in < 500 ms

    marks = Column(Integer, nullable=True)