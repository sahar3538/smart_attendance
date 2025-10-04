
import os
import csv
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QCalendarWidget, QMessageBox, QTableWidget, QTableWidgetItem
)
from PyQt5.QtCore import Qt

from data_manager import load_schedule, save_schedule, get_attendance_summary, load_students

class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Teacher - Manage Attendance")
        self.setFixedSize(1000, 600)

        layout = QVBoxLayout()

        self.subject_label = QLabel("Subject:")
        layout.addWidget(self.subject_label)

        self.subject_input = QListWidget()
        subjects = sorted(set([s[2] for s in load_students()]))
        self.subject_input.addItems(subjects)
        layout.addWidget(self.subject_input)

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)

        set_btn = QPushButton("Schedule Attendance for Selected Date")
        set_btn.clicked.connect(self.schedule_date)
        layout.addWidget(set_btn)

        view_btn = QPushButton("View Attendance Summary")
        view_btn.clicked.connect(self.view_summary)
        layout.addWidget(view_btn)

        self.result_label = QLabel("")
        layout.addWidget(self.result_label)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def schedule_date(self):
        subject = self.get_selected_subject()
        if not subject:
            return

        date = self.calendar.selectedDate().toString("yyyy-MM-dd")
        schedule = load_schedule()
        if subject not in schedule:
            schedule[subject] = []
        if date not in schedule[subject]:
            schedule[subject].append(date)
            save_schedule(schedule)
            QMessageBox.information(self, "Scheduled", f"Date {date} scheduled for {subject}")
        else:
            QMessageBox.information(self, "Already Scheduled", f"Date {date} already exists.")

    def view_summary(self):
        subject = self.get_selected_subject()
        if not subject:
            return

        students = [sid for sid, _, subj in load_students() if subj == subject]
        today = datetime.now().strftime("%Y-%m-%d")
        schedule = [d for d in load_schedule().get(subject, []) if d <= today]        
        attendance_file = f"attendance/{subject}.csv"

        # Build student-day attendance
        attendance_map = {sid: {date: "Absent" for date in schedule} for sid in students}
        if os.path.exists(attendance_file):
            with open(attendance_file, "r") as f:
                for line in f:
                    date, sid, status = line.strip().split(",")
                    if sid in attendance_map and date in schedule:
                        attendance_map[sid][date] = status

        # Setup table widget
        if hasattr(self, "summary_table"):
            self.layout().removeWidget(self.summary_table)
            self.summary_table.deleteLater()

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(len(schedule) + 2)
        headers = ["Student ID"] + schedule + ["% Present"]
        self.summary_table.setHorizontalHeaderLabels(headers)
        self.summary_table.setRowCount(len(students))

        for row_idx, sid in enumerate(students):
            self.summary_table.setItem(row_idx, 0, QTableWidgetItem(sid))
            present_count = 0
            for col_idx, date in enumerate(schedule, start=1):
                status = attendance_map[sid][date]
                if status == "Present":
                    present_count += 1
                self.summary_table.setItem(row_idx, col_idx, QTableWidgetItem(status))
            percent = (present_count / len(schedule)) * 100 if schedule else 0
            self.summary_table.setItem(row_idx, len(schedule)+1, QTableWidgetItem(f"{percent:.2f}%"))

        self.layout().addWidget(self.summary_table)

        # Optional: Save to CSV
        save_path = f"attendance/{subject}_summary.csv"
        with open(save_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for sid in students:
                row = [sid] + [attendance_map[sid][d] for d in schedule]
                present = sum(1 for d in schedule if attendance_map[sid][d] == "Present")
                percent = (present / len(schedule)) * 100 if schedule else 0
                row.append(f"{percent:.2f}%")
                writer.writerow(row)

        QMessageBox.information(self, "Done", f"Summary saved as '{save_path}'")


    def get_selected_subject(self):
        selected = self.subject_input.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Select Subject", "Please select a subject.")
            return None
        return selected[0].text()
    def go_back(self):
        from ui.role_selection import RoleSelectionWindow  # ✅ lazy import
        self.role = RoleSelectionWindow()
        self.role.show()
        self.close()