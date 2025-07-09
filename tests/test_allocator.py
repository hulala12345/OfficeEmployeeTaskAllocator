import os
import tempfile
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from task_allocator import db, allocator


def setup_module(module):
    # Use a temporary database
    db.DB_PATH = tempfile.gettempdir() + '/test_task_allocator.db'
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)
    db.init_db()


def teardown_module(module):
    if os.path.exists(db.DB_PATH):
        os.remove(db.DB_PATH)


def test_assignment():
    db.add_employee('Alice', ['python', 'docs'])
    db.add_employee('Bob', ['python'])
    db.add_task('Write docs', 'Doc task', ['docs'], '2099-01-01', 3)
    assignments = allocator.assign_tasks()
    assert len(assignments) == 1
    task = db.list_tasks()[0]
    assert task['employee_id'] is not None

