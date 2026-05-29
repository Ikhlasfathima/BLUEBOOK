from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import SessionLocal

SECRET_KEY         = "bluebook-secret-key-2026-do-not-share"
ALGORITHM          = "HS256"
TOKEN_EXPIRE_HOURS = 24

# ── Password hashing ──────────────────────────────────────────────────────────
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    pwd_context.hash("test")  # test it works

    def hash_password(plain: str) -> str:
        return pwd_context.hash(plain)

    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)

except Exception:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def hash_password(plain: str) -> str:
        return pwd_context.hash(plain)

    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)


# ── JWT ───────────────────────────────────────────────────────────────────────
def create_access_token(data: dict) -> str:
    payload = data.copy()
    # Store sub as string to avoid type issues on decode
    payload["sub"] = str(payload["sub"])
    payload["exp"] = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ── Dependencies ──────────────────────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    from models import User
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exc
        user_id = int(user_id)  # convert back from string
    except (JWTError, ValueError):
        raise credentials_exc

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exc
    return user


# ── Role guards ───────────────────────────────────────────────────────────────
def require_teacher(current_user=Depends(get_current_user)):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    return current_user

def require_student(current_user=Depends(get_current_user)):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Students only")
    return current_user