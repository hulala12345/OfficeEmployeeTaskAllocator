import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'task_allocator.db'


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            skills TEXT NOT NULL
        )"""
    )
    c.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            skills TEXT NOT NULL,
            deadline TEXT,
            est_time REAL,
            status TEXT DEFAULT 'not started',
            employee_id INTEGER,
            assigned_at TEXT,
            completed_at TEXT,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )"""
    )
    conn.commit()
    conn.close()



def add_employee(name: str, skills: list[str]):
    conn = get_connection()
    c = conn.cursor()
    skills_str = ','.join(skills)
    c.execute("INSERT INTO employees (name, skills) VALUES (?, ?)", (name, skills_str))
    conn.commit()
    conn.close()


def list_employees():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, skills FROM employees")
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append({'id': row[0], 'name': row[1], 'skills': row[2].split(',')})
    return result


def add_task(title: str, description: str, skills: list[str], deadline: str, est_time: float):
    conn = get_connection()
    c = conn.cursor()
    skills_str = ','.join(skills)
    c.execute(
        "INSERT INTO tasks (title, description, skills, deadline, est_time) VALUES (?, ?, ?, ?, ?)",
        (title, description, skills_str, deadline, est_time),
    )
    conn.commit()
    conn.close()


def list_tasks():
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id, title, description, skills, deadline, est_time, status, employee_id, assigned_at, completed_at FROM tasks"
    )
    rows = c.fetchall()
    conn.close()
    result = []
    for row in rows:
        result.append(
            {
                'id': row[0],
                'title': row[1],
                'description': row[2],
                'skills': row[3].split(','),
                'deadline': row[4],
                'est_time': row[5],
                'status': row[6],
                'employee_id': row[7],
                'assigned_at': row[8],
                'completed_at': row[9],
            }
        )
    return result


def update_task_status(task_id: int, status: str, completed_at: str | None = None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=?, completed_at=? WHERE id=?", (status, completed_at, task_id))
    conn.commit()
    conn.close()

