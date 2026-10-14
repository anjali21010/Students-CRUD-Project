from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date
import sqlite3

app = FastAPI(
    title="Students Database CRUD Application",
    description="EWB Python Backend Development Internship Project",
    version="1.0.0"
)

DATABASE = "students.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date_of_birth TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                course TEXT,
                address TEXT,
                enrollment_date TEXT
            )
        """)


initialize_database()


class StudentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    date_of_birth: date
    email: EmailStr
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    course: Optional[str] = None
    address: Optional[str] = None
    enrollment_date: Optional[date] = None


def student_dict(row):
    return dict(row)


@app.get("/")
def home():
    return {"message": "Students CRUD API is running!"}


@app.post("/students", status_code=201)
def create_student(student: StudentCreate):
    data = student.model_dump(mode="json")
    try:
        with get_connection() as connection:
            cursor = connection.execute("""
                INSERT INTO students
                (name, date_of_birth, email, phone, course, address, enrollment_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data["name"], data["date_of_birth"], data["email"],
                data["phone"], data["course"], data["address"],
                data["enrollment_date"]
            ))
            row = connection.execute(
                "SELECT * FROM students WHERE id = ?", (cursor.lastrowid,)
            ).fetchone()
            return student_dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists.")


@app.get("/students")
def list_students(
    name: Optional[str] = Query(default=None),
    course: Optional[str] = Query(default=None)
):
    with get_connection() as connection:
        query = "SELECT * FROM students WHERE 1=1"
        parameters = []

        if name:
            query += " AND name LIKE ?"
            parameters.append(f"%{name}%")

        if course:
            query += " AND course LIKE ?"
            parameters.append(f"%{course}%")

        rows = connection.execute(query, parameters).fetchall()
        return [student_dict(row) for row in rows]


@app.get("/students/{student_id}")
def get_student(student_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM students WHERE id = ?", (student_id,)
        ).fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Student not found.")

    return student_dict(row)


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentUpdate):
    data = student.model_dump(exclude_unset=True, mode="json")

    if not data:
        raise HTTPException(status_code=400, detail="No fields provided.")

    if any(value is None for value in data.values()):
        raise HTTPException(status_code=400, detail="Fields cannot be set to null.")

    allowed_fields = {
        "name", "date_of_birth", "email", "phone",
        "course", "address", "enrollment_date"
    }

    if not set(data).issubset(allowed_fields):
        raise HTTPException(status_code=400, detail="Invalid fields.")

    assignments = ", ".join(f"{field} = ?" for field in data)
    values = list(data.values())

    try:
        with get_connection() as connection:
            existing = connection.execute(
                "SELECT id FROM students WHERE id = ?", (student_id,)
            ).fetchone()

            if existing is None:
                raise HTTPException(status_code=404, detail="Student not found.")

            connection.execute(
                f"UPDATE students SET {assignments} WHERE id = ?",
                values + [student_id]
            )
            row = connection.execute(
                "SELECT * FROM students WHERE id = ?", (student_id,)
            ).fetchone()
            return student_dict(row)
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Email already exists.")


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM students WHERE id = ?", (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found.")

    return {"message": f"Student {student_id} deleted successfully."}