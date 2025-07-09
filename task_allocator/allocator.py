from __future__ import annotations
import datetime
from . import db


def assign_tasks(current_time: str | None = None):
    """Assign unassigned tasks to employees based on skills and workload."""
    employees = db.list_employees()
    tasks = [t for t in db.list_tasks() if t['employee_id'] is None]
    if not employees or not tasks:
        return []
    current_time = current_time or datetime.datetime.utcnow().isoformat()

    # Calculate workload per employee (sum of est_time for not completed tasks)
    workload = {e['id']: 0.0 for e in employees}
    for t in db.list_tasks():
        if t['employee_id'] and t['status'] != 'completed':
            workload[t['employee_id']] += t['est_time']

    assignments = []
    for task in tasks:
        # Find employees with required skill
        candidates = [e for e in employees if set(task['skills']).issubset(set(e['skills']))]
        if not candidates:
            continue
        # Choose employee with minimal workload
        employee = min(candidates, key=lambda e: workload[e['id']])
        # Update database
        conn = db.get_connection()
        c = conn.cursor()
        c.execute(
            "UPDATE tasks SET employee_id=?, status='in progress', assigned_at=? WHERE id=?",
            (employee['id'], current_time, task['id']),
        )
        conn.commit()
        conn.close()
        workload[employee['id']] += task['est_time']
        assignments.append((task['id'], employee['id']))
    return assignments

