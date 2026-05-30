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
## Screenshots

### Student Login Page
<img width="1919" height="868" alt="Screenshot 2026-05-09 174715" src="https://github.com/user-attachments/assets/33c5e139-c0be-4a5c-9c6d-30ca39659ef8" />

### Teacher Login Page
<img width="1918" height="866" alt="Screenshot 2026-05-10 212812" src="https://github.com/user-attachments/assets/9b7d1434-4dea-4608-96a9-9e112e9fd032" />

### Teacher Dashboard
<img width="1917" height="865" alt="Screenshot 2026-05-09 175033" src="https://github.com/user-attachments/assets/7cf332a5-8f2f-4fe6-9742-bca78814b028" />

### Student Dashboard
<img width="1915" height="861" alt="Screenshot 2026-05-09 174910" src="https://github.com/user-attachments/assets/2f47d99c-5f5e-4092-95ef-438526018524" />

### Assignment View By Students
<img width="1918" height="868" alt="Screenshot 2026-05-09 174958" src="https://github.com/user-attachments/assets/c23d35be-eba9-40b0-9b59-a0c3f048efc9" />

### Editor for Students with Copy-Paste Detection
<img width="1911" height="869" alt="Screenshot 2026-05-10 213534" src="https://github.com/user-attachments/assets/a30f68be-b1ec-4629-b21b-891123b5735b" />

### Assignment Evaluation By Teachers
<img width="1914" height="870" alt="Screenshot 2026-05-10 214426" src="https://github.com/user-attachments/assets/1411436e-23a8-4f8a-8990-dd2d54aaf394" />
<img width="455" height="122" alt="Screenshot 2026-05-10 214650" src="https://github.com/user-attachments/assets/a4196381-fc55-44df-8ad7-1c8b99bbbca6" />
<img width="913" height="171" alt="Screenshot 2026-05-10 214759" src="https://github.com/user-attachments/assets/cbc1e9d8-3f81-4443-9344-a2ebbef47956" />

### AI Generated Summary for Teachers
<img width="922" height="364" alt="Screenshot 2026-05-10 214907" src="https://github.com/user-attachments/assets/da5e7673-95f9-4930-a5d7-6762e1d3a936" />

## Docker Setup

### Build Containers

```bash
docker compose up --build
```

### Stop Containers

```bash<img width="455" height="122" alt="Screenshot 2026-05-10 214650" src="https://github.com/user-attachments/assets/7c385d6b-1fe6-4b90-8a21-9b7ee7ec3da4" />

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
