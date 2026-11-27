import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QLineEdit, QListWidget, QVBoxLayout, QWidget


class WindowGUI(QWidget):

  def __init__(self):
    super().__init__()
    self.init_ui()

  def init_ui(self):
    # Window
    self.setWindowFlags(
        Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint
    )
    self.resize(800, 450)

    # UI 
    self.search_input = QLineEdit()
    self.search_input.setPlaceholderText("Type here")  

    self.result_list = QListWidget()
    
    self.result_list.addItems(["Test Filter 1", "Test Filter 2"])

    self.info_label = QLabel("output")  
    self.info_label.setWordWrap(True)  

    # Layer
    layout = QVBoxLayout()
    layout.addWidget(self.search_input)  # Top
    layout.addWidget(self.result_list)  # Mid
    layout.addWidget(self.info_label)  # Tail
    self.setLayout(layout)

  # 4. esc escape
  def keyPressEvent(self, event):
    if event.key() == Qt.Key.Key_Escape:  
      self.close()


if __name__ == "__main__":
  app = QApplication(sys.argv)
  window = WindowGUI()
  window.show()
  sys.exit(app.exec())