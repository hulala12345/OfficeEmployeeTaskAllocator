import argparse
import datetime
from . import db, allocator, reports


def main():
    parser = argparse.ArgumentParser(description="Office Employee Task Allocator")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="initialize database")

    emp_parser = sub.add_parser("add-employee", help="add employee")
    emp_parser.add_argument("name")
    emp_parser.add_argument("skills", nargs="+")

    task_parser = sub.add_parser("add-task", help="add task")
    task_parser.add_argument("title")
    task_parser.add_argument("description")
    task_parser.add_argument("skills", nargs="+")
    task_parser.add_argument("deadline")
    task_parser.add_argument("est_time", type=float)

    sub.add_parser("assign", help="run assignment algorithm")
    sub.add_parser("list-tasks", help="list all tasks")
    sub.add_parser("list-employees", help="list all employees")
    sub.add_parser("report", help="show reports")

    args = parser.parse_args()

    if args.command == "init":
        db.init_db()
        print("Database initialized")
    elif args.command == "add-employee":
        db.add_employee(args.name, args.skills)
        print("Employee added")
    elif args.command == "add-task":
        db.add_task(args.title, args.description, args.skills, args.deadline, args.est_time)
        print("Task added")
    elif args.command == "assign":
        assigned = allocator.assign_tasks()
        for task_id, emp_id in assigned:
            print(f"Task {task_id} assigned to employee {emp_id}")
        if not assigned:
            print("No tasks assigned")
    elif args.command == "list-tasks":
        for t in db.list_tasks():
            print(t)
    elif args.command == "list-employees":
        for e in db.list_employees():
            print(e)
    elif args.command == "report":
        wd = reports.workload_distribution()
        tc = reports.task_completion_report()
        dl = reports.deadline_compliance_report()
        print("Workload:", wd)
        print("Completion:", tc)
        print("Deadline Compliance:", dl)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

