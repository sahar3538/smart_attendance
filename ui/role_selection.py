from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from ui.admin_window import AdminWindow
from ui.teacher_window import TeacherWindow
from ui.student_window import StudentWindow

class RoleSelectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Select Role")
        self.setFixedSize(1000, 600)
        layout = QVBoxLayout()

        label = QLabel("Who are you?")
        label.setFont(QFont("Arial", 14))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        admin_btn = QPushButton("Admin")
        admin_btn.clicked.connect(self.open_admin)
        layout.addWidget(admin_btn)

        teacher_btn = QPushButton("Teacher")
        teacher_btn.clicked.connect(self.open_teacher)
        layout.addWidget(teacher_btn)

        student_btn = QPushButton("Student")
        student_btn.clicked.connect(self.open_student)
        layout.addWidget(student_btn)

        self.setLayout(layout)

    def open_admin(self):
        self.window = AdminWindow()
        self.window.show()
        self.close()

    def open_teacher(self):
        self.window = TeacherWindow()
        self.window.show()
        self.close()

    def open_student(self):
        self.window = StudentWindow()
        self.window.show()
        self.close()
