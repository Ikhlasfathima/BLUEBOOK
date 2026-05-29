import sys
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, teacher, student
from database import engine
import models

# Creates all tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="."), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(teacher.router)
app.include_router(student.router)

@app.get("/editor")
def editor_page():
    return FileResponse("editor.html")

@app.get("/teacher")
def teacher_page():
    return FileResponse("teacher.html")

@app.get("/marks")
def marks_page():
    return FileResponse("marks.html")

# Health check — visit http://127.0.0.1:8000/ to confirm server is up
@app.get("/")
def home():
    return FileResponse("auth.html")