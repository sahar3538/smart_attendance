from PyQt5.QtWidgets import QApplication
import sys
from ui.role_selection import RoleSelectionWindow

app = QApplication(sys.argv)
window = RoleSelectionWindow()
window.show()
sys.exit(app.exec_())
