# Students Database CRUD Application

## Project Overview
This project is a Students Database CRUD Application developed using Python, FastAPI, and SQLite. It allows users to create, view, update, and delete student records through a REST API.

## Features
- Add new student records
- View all students
- View a student by ID
- Update student details
- Delete student records
- Search students by name or course
- Store student data in an SQLite database
- Validate student details such as email and date of birth

## Technologies Used
- Python
- FastAPI
- SQLite
- Pydantic
- Uvicorn
- Swagger UI

## Student Details
The application supports the following fields:
- Student ID
- Name
- Date of Birth
- Email
- Phone
- Course
- Address
- Enrollment Date

## Installation and Setup

1. Install Python on your computer.
2. Open the project folder in VS Code.
3. Open the terminal in VS Code.
4. Install the required packages:

```bash
python -m pip install -r requirements.txt
```

5. Start the application:

```bash
python -m uvicorn main:app --reload
```

6. Open the following URL in your browser:

`http://127.0.0.1:8000/docs`

Use the Swagger UI interface to test the API endpoints.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/students` | Create a student |
| GET | `/students` | View all students |
| GET | `/students/{student_id}` | View a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |
| GET | `/` | Check API status |

## Database
The application uses SQLite. The `students.db` database file is created automatically when the application runs.

## Project Status
The CRUD operations have been tested successfully using Swagger UI.

## Author
Python Backend Development Internship Project
