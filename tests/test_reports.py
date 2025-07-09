import os
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from task_allocator import db, allocator, reports


def setup_module(module):
    db.DB_PATH = tempfile.gettempdir() + '/test_task_allocator.db'
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()


def teardown_module(module):
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)


def test_reports():
    db.add_employee('Alice', ['python'])
    db.add_task('Task', 'Desc', ['python'], '2099-01-01', 2)
    allocator.assign_tasks(current_time='2024-01-01T00:00:00')
    db.update_task_status(1, 'completed', completed_at='2024-01-02T00:00:00')
    workload = reports.workload_distribution()
    assert workload['Alice'] == 0
    comp = reports.task_completion_report()
    assert comp['completed_tasks'] == 1
    dl = reports.deadline_compliance_report()
    assert dl['tasks_with_deadline'] == 1

