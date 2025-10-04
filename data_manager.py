import os
import csv
import json
from datetime import datetime
from collections import defaultdict

STUDENT_FILE = "students.csv"
SCHEDULE_FILE = "schedule.json"

def save_student(student_id, name, subject):
    file_path = "students.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True) if "/" in file_path else None

    existing = load_students()
    if [student_id, name, subject] in existing:
        return False  # Already exists

    with open(file_path, "a") as f:
        f.write(f"{student_id},{name},{subject}\n")
    return True

def load_students():
    if not os.path.exists(STUDENT_FILE):
        return []
    with open(STUDENT_FILE, "r") as f:
        return [line.strip().split(",") for line in f if line.strip()]

def write_attendance(student_id, subject, status):
    os.makedirs("attendance", exist_ok=True)
    file_path = f"attendance/{subject}.csv"
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(file_path, "a") as f:
        f.write(f"{date_str},{student_id},{status}\n")

def load_schedule():
    if not os.path.exists(SCHEDULE_FILE):
        return {}
    with open(SCHEDULE_FILE, "r") as f:
        return json.load(f)

def save_schedule(schedule):
    with open(SCHEDULE_FILE, "w") as f:
        json.dump(schedule, f, indent=2)

def get_attendance_summary(subject):
    summary = defaultdict(lambda: {"Present": 0, "Total": 0})
    schedule = load_schedule().get(subject, [])
    attendance_file = f"attendance/{subject}.csv"

    if not os.path.exists(attendance_file):
        return summary, len(schedule)

    with open(attendance_file, "r") as f:
        for line in f:
            date, student_id, status = line.strip().split(",")
            if date in schedule:
                summary[student_id]["Total"] += 1
                if status == "Present":
                    summary[student_id]["Present"] += 1

    return summary, len(schedule)
