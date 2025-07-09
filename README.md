# Office Employee Task Allocator

This project provides a simple command line application for managing office tasks and employees.

Features include:
- Create employee profiles with skills.
- Create tasks with required skills, deadlines and estimated times.
- Automatically assign tasks to available employees based on their skills and workload.
- Track task status and generate reports on workload distribution and completion rates.

## Quick Start

```
python -m task_allocator.interface init
python -m task_allocator.interface add-employee "Alice" programming documentation
python -m task_allocator.interface add-task "Write report" "Quarterly report" documentation 2024-05-01 4
python -m task_allocator.interface assign
python -m task_allocator.interface list-tasks
python -m task_allocator.interface report
```

The application stores data in a local SQLite database `task_allocator.db` created in the package directory.
