"""
auth.py — signup / login with bcrypt + JWT
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, LoginRequest
from security import hash_password, verify_password, create_access_token, get_db

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username = user.username,
        email    = user.email,
        password = hash_password(user.password),   # ← hashed, never plain text
        role     = user.role,
        class_id = user.class_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "Signup successful", "user_id": new_user.id}


@router.post("/login")
def login(body: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == body.username).first()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.id, "role": user.role})

    return {
        "access_token" : token,
        "token_type"   : "bearer",
        # frontend convenience fields (non-sensitive)
        "id"       : user.id,
        "username" : user.username,
        "role"     : user.role,
        "class_id" : user.class_id,
    }


# Dev-only — remove in production
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()