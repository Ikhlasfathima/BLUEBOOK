# BLUEBOOK – Digital Assignment Management System

## Overview

BLUEBOOK is a web-based assignment management platform developed to modernize and simplify the assignment submission and evaluation process in educational institutions.

The system provides separate interfaces for students and teachers. Students can write assignments using a rich text editor, submit responses, and view their marks. Teachers can create assignments, review submissions, analyze writing behavior, generate AI-powered summaries, and assign marks.

The project also includes typing behavior analytics to differentiate between genuinely typed content and pasted content, helping teachers identify suspicious submissions.

---

## Key Features

### Student Features

- Student Registration and Login
- JWT-Based Authentication
- Rich Text Assignment Editor
- Assignment Submission System
- View Assigned Tasks
- View Marks and Feedback
- Typing vs Pasting Detection
- Writing Behavior Tracking

### Teacher Features

- Teacher Registration and Login
- Create Assignments
- View Student Submissions
- Generate AI Summaries
- Evaluate Student Responses
- Assign Marks
- View Submission Analytics
- Detect High Pasted Content

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript

### Backend

- FastAPI
- SQLAlchemy ORM
- JWT Authentication
- Passlib (Password Hashing)

### Database

- PostgreSQL
- SQLite (used during initial development)

### AI Integration

- Google Gemini API

### DevOps

- Docker
- Docker Compose

---

## System Workflow

### Student Workflow

1. Student creates an account.
2. Student logs into the system.
3. Student views available assignments.
4. Student selects an assignment.
5. Student writes the response using the editor.
6. Typing and pasting behavior is tracked.
7. Assignment is submitted and stored in the database.
8. Student can view assigned marks.

### Teacher Workflow

1. Teacher creates an account.
2. Teacher logs into the system.
3. Teacher creates assignments for a class.
4. Students submit responses.
5. Teacher reviews submissions.
6. System displays analytics:
   - Typed Percentage
   - Pasted Percentage
   - Typing Speed
   - Typing Variance
   - Pause Count
   - Backspace Count
   - Burst Typing Events
7. Gemini AI generates a summary.
8. Teacher assigns marks.

---

## Typing Behaviour Analytics

The system tracks several writing metrics:

- Typed Character Count
- Pasted Character Count
- Average Typing Speed
- Typing Variance
- Pause Detection
- Backspace Count
- Burst Typing Events

These metrics help teachers evaluate the authenticity of student work.

---

## Security Features

### Password Hashing

Passwords are hashed using Passlib before being stored in the database.

### JWT Authentication

JSON Web Tokens (JWT) are used for:

- User Authentication
- Protected Routes
- Session Management

### Role-Based Access

The system supports:

- Student Role
- Teacher Role

Each role can access only the relevant pages and APIs.

---

## Project Structure

```text
BLUEBOOK/
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── student.py
│   └── teacher.py
│
├── .env
├── .gitignore
├── auth.html
├── database.db
├── database.py
├── docker-compose.yml
├── Dockerfile
├── editor.html
├── main.py
├── marks.html
├── models.py
├── README.md
├── requirements.txt
├── schemas.py
├── security.py
└── teacher.html
```

---

## Database Tables

### Users

Stores:

- Username
- Email
- Password Hash
- Role
- Class ID

### Assignments

Stores:

- Assignment Title
- Class ID
- Deadline
- Maximum Marks

### Submissions

Stores:

- Student Response
- Typing Analytics
- AI Summary
- Marks

---

## API Endpoints

### Authentication

- POST /signup
- POST /login
- GET /users

### Teacher Operations

- Create Assignment
- View Submissions
- Generate AI Summary
- Assign Marks

### Student Operations

- View Assignments
- Submit Assignment
- View Marks

---

## Docker Setup

### Build Containers

```bash
docker compose up --build
```

### Stop Containers

```bash
docker compose down
```

### View Running Containers

```bash
docker ps
```

---

## Running Locally

### Backend

```bash
uvicorn main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

### Frontend

```bash
python -m http.server 8001
```

Frontend URL:

```text
http://localhost:8001/auth.html
```

---

## Future Enhancements

- AI-Based Plagiarism Detection
- Real-Time Typing Monitoring
- PDF Assignment Upload Support
- Assignment Notifications
- Email Integration
- Advanced Teacher Dashboard
- Student Performance Analytics
- Multi-Class Management
- Cloud Deployment
- Mobile Responsive Design

---

## Learning Outcomes

Through this project, the following concepts were implemented and explored:

- REST API Development
- FastAPI Framework
- SQLAlchemy ORM
- JWT Authentication
- Database Design
- Docker Containerization
- PostgreSQL Integration
- AI API Integration
- Frontend and Backend Communication
- Rich Text Editing
- Writing Behaviour Analytics

---

## Author

**Ikhlas Fathima**

BLUEBOOK – Digital Assignment Management System

Developed as a full-stack web application using FastAPI, SQLAlchemy, PostgreSQL, Docker, JWT Authentication, and Google Gemini AI.