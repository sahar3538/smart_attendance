from PyQt5.QtWidgets import *
import cv2
import os
import csv
from datetime import datetime
from face_utils import MODEL_PATH, face_cascade, get_face_id
from data_manager import load_schedule, write_attendance, load_students

class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student - Mark Attendance")
        self.setFixedSize(1000, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Enter Student ID:"))
        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)

        mark_btn = QPushButton("Mark Attendance")
        mark_btn.clicked.connect(self.mark_attendance)
        layout.addWidget(mark_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def mark_attendance(self):
        student_id = self.id_input.text().strip()
        if not student_id:
            QMessageBox.warning(self, "Missing", "Enter your student ID.")
            return

        subject = self.get_subject_by_id(student_id)
        if not subject:
            QMessageBox.warning(self, "Not Found", "Student ID not found.")
            return

        today = datetime.now().strftime("%Y-%m-%d")
        scheduled = load_schedule().get(subject, [])
        if today not in scheduled:
            QMessageBox.warning(self, "Not Scheduled", f"No attendance scheduled today for {subject}.")
            return

        if not os.path.exists(MODEL_PATH):
            QMessageBox.warning(self, "Model Missing", "Face model not trained yet.")
            return

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(MODEL_PATH)

        cap = cv2.VideoCapture(0)
        marked = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                label, conf = recognizer.predict(face_img)
                predicted_id = str(label)

                if conf < 70 and predicted_id == student_id:
                    write_attendance(student_id, subject, "Present")
                    QMessageBox.information(self, "Marked", f"Attendance marked for {student_id}")
                    marked = True
                    break
                else:
                    cv2.putText(frame, "Unknown", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            cv2.imshow("Mark Attendance", frame)
            if marked or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if not marked:
            QMessageBox.information(self, "Failed", "Face not recognized.")

    def get_subject_by_id(self, student_id):
        for sid, _, subject in load_students():
            if sid == student_id:
                return subject
        return None
    def go_back(self):
        from ui.role_selection import RoleSelectionWindow  # ✅ lazy import
        self.role = RoleSelectionWindow()
        self.role.show()
        self.close()
