from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QFont

class Сriterion(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        #self.setCheckable(True)
        self.setFont(QFont('Arial', 20))
        
        self.setStyleSheet('''
            QPushButton {
                background-color: #9fb3a7;
                border-style: outset;
                border-width: 1px;
                border-radius: 6px;
                border-color: #000000;
                font: 16px;
                padding: 12px;
            }
            QPushButton:checked {
                background-color: #6ceb9f;
                border-style: inset;
            }
            QPushButton:hover {
                color: white;
            }
            
            QPushButton:disabled  {
                
                background-color: #6ceb9f;
                color: black;
            }
        ''')
class Submits(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        #self.setCheckable(True)
        #self.setFont(QFont('Arial', 20))
        
        self.setStyleSheet(
            """QPushButton {
                border: 1px solid black;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #6ceb9f
            }
            
            """)