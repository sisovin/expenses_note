from PyQt6.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from database import delete_expense

class DeleteExpenseDialog(QDialog):
    def __init__(self, expense_id, parent=None):
        super().__init__(parent)
        self.expense_id = expense_id
        self.setWindowTitle("Delete Expense")
        self.setGeometry(800, 400, 300, 150)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        label = QLabel("Are you sure you want to delete this record?")
        layout.addWidget(label)
        
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        button_layout.addStretch()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        self.ok_button.clicked.connect(self.delete_expense)
        self.cancel_button.clicked.connect(self.reject)

    def delete_expense(self):
        if delete_expense(self.expense_id):
            QMessageBox.information(self, "Success", "Expense deleted successfully.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to delete expense.")