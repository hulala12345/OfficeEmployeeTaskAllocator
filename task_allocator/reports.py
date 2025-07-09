from __future__ import annotations
import datetime
from . import db


def workload_distribution():
    employees = db.list_employees()
    tasks = db.list_tasks()
    workload = {e['name']: 0.0 for e in employees}
    for task in tasks:
        if task['employee_id'] and task['status'] != 'completed':
            emp = next((e for e in employees if e['id'] == task['employee_id']), None)
            if emp:
                workload[emp['name']] += task['est_time']
    return workload


def task_completion_report(start: str | None = None, end: str | None = None):
    tasks = db.list_tasks()
    fmt = "%Y-%m-%d"
    if start:
        start_dt = datetime.datetime.strptime(start, fmt)
        tasks = [t for t in tasks if t['completed_at'] and datetime.datetime.fromisoformat(t['completed_at']).date() >= start_dt.date()]
    if end:
        end_dt = datetime.datetime.strptime(end, fmt)
        tasks = [t for t in tasks if t['completed_at'] and datetime.datetime.fromisoformat(t['completed_at']).date() <= end_dt.date()]

    completed = [t for t in tasks if t['status'] == 'completed']
    total = len(tasks)
    rate = len(completed) / total if total else 0
    return {
        'total_tasks': total,
        'completed_tasks': len(completed),
        'completion_rate': rate,
    }


def deadline_compliance_report():
    tasks = db.list_tasks()
    on_time = 0
    with_deadline = [t for t in tasks if t['deadline']]
    for task in with_deadline:
        if task['completed_at'] and task['completed_at'] <= task['deadline']:
            on_time += 1
    return {
        'tasks_with_deadline': len(with_deadline),
        'completed_on_time': on_time,
    }

