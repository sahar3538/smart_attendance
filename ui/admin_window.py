from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
)
from face_utils import capture_faces, train_faces
from data_manager import save_student
from face_utils import face_cascade

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin - Register Students")
        self.setFixedSize(1000, 600)
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Student ID:"))
        self.id_input = QLineEdit()
        layout.addWidget(self.id_input)

        layout.addWidget(QLabel("Student Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)

        layout.addWidget(QLabel("Subject:"))
        self.subject_input = QLineEdit()
        layout.addWidget(self.subject_input)

        capture_btn = QPushButton("Capture Faces")
        capture_btn.clicked.connect(self.capture_faces)
        layout.addWidget(capture_btn)

        train_btn = QPushButton("Train Model")
        train_btn.clicked.connect(self.train_model)
        layout.addWidget(train_btn)
         

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.go_back)
        layout.addWidget(back_btn)

        self.setLayout(layout)

    def capture_faces(self):
        student_id = self.id_input.text().strip()
        name = self.name_input.text().strip()
        subject = self.subject_input.text().strip()

        if not student_id or not name or not subject:
            QMessageBox.warning(self, "Missing Info", "Please enter all fields.")
            return

        added = save_student(student_id, name, subject)
        if not added:
            QMessageBox.information(self, "Exists", "Student already registered for this subject.")
            return

        count = capture_faces(student_id, subject)
        QMessageBox.information(self, "Captured", f"{count} face images captured for {name}.")


    def train_model(self):
        train_faces()
        QMessageBox.information(self, "Success", "Model trained successfully!")

    def go_back(self):
        from ui.role_selection import RoleSelectionWindow  # ✅ lazy import
        self.role = RoleSelectionWindow()
        self.role.show()
        self.close()
