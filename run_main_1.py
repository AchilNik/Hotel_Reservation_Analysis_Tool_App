from PyQt5.QtWidgets import QApplication
from main_1 import MyApp
import sys

app = QApplication(sys.argv)
window = MyApp()
sys.exit(app.exec_())
