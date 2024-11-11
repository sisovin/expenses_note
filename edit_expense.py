from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QComboBox, QDateEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QDate
from database import fetch_expenses, update_expense, fetch_categories

class EditExpenseDialog(QDialog):
    def __init__(self, expense_id, parent=None):
        super().__init__(parent)
        self.expense_id = expense_id
        self.setWindowTitle("Edit Expense")
        self.setGeometry(800, 400, 400, 300)
        self.initUI()
        self.load_expense_data()

    def initUI(self):
        # Create layout
        layout = QVBoxLayout()

        # Create form fields
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.category_combo = QComboBox()
        self.amount_edit = QLineEdit()
        self.description_edit = QLineEdit()

        # Populate category combo box
        self.populate_categories()

        # Create buttons
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")

        # Connect buttons
        self.save_button.clicked.connect(self.save_expense)
        self.cancel_button.clicked.connect(self.reject)

        # Add widgets to layout
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(self.date_edit)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(self.category_combo)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(self.amount_edit)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(self.description_edit)

        # Add buttons to layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def populate_categories(self):
        categories = fetch_categories()
        for category in categories:
            self.category_combo.addItem(category[1], category[0])

    def load_expense_data(self):
        expenses = fetch_expenses()
        for expense in expenses:
            if expense[0] == self.expense_id:
                self.date_edit.setDate(QDate.fromString(expense[1], Qt.DateFormat.ISODate))
                self.category_combo.setCurrentText(expense[2])
                self.amount_edit.setText(str(expense[3]))
                self.description_edit.setText(expense[4])
                break

    def save_expense(self):
        date = self.date_edit.date().toString(Qt.DateFormat.ISODate)
        category_id = self.category_combo.currentData()
        amount = float(self.amount_edit.text())
        description = self.description_edit.text()

        if update_expense(self.expense_id, date, category_id, amount, description):
            QMessageBox.information(self, "Success", "Expense updated successfully.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Failed to update expense.")

# Example usage
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = EditExpenseDialog(1)  # Pass the expense ID you want to edit
    dialog.exec()