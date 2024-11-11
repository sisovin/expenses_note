from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QDateEdit, QTableWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem, QHeaderView, QFrame
from PyQt6.QtCore import Qt, QDate
from database import add_expense, fetch_expenses, update_expense, delete_expense, fetch_categories
from edit_expense import EditExpenseDialog
from delete_expense import DeleteExpenseDialog
from category import CategoryDialog
from functools import partial

class ExpenseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.intUI()
        
    def settings(self):       
        self.setWindowTitle("Expense Notebook App")
        self.setGeometry(750, 300, 550, 500)
    
    # Design the UI App
    def intUI(self):
        # Create all Objects
        ## Elements for adding an expense
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.dropdown = QComboBox()
        self.amount = QLineEdit()
        self.description = QLineEdit()
        
        ## Elements for the button App
        self.btn_add = QPushButton("Add Expense")
        self.btn_add.clicked.connect(self.add_expense)
        
        ## Elements for the Table
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["ID", "Date", "Category", "Amount", "Description", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Populate the Dropdown
        self.populate_dropdown()
        
        ## Add Widgets to the Layout
        self.setup_layout()
        self.refresh_table()
        
    # Set Layouts
    def setup_layout(self):
        # Create a master Layout
        master = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        
        ## Start Row 1 What you want to see
        row1.addWidget(QLabel("Date:"))
        row1.addWidget(self.date_box)
        row1.addWidget(QLabel("Category:"))
        row1.addWidget(self.dropdown)
        
        ## Start Row 2 What you want to see
        row2.addWidget(QLabel("Amount:"))
        row2.addWidget(self.amount)
        row2.addWidget(QLabel("Description:"))
        row2.addWidget(self.description)
        
        ## Start Row 3 What you want to see
        row3.addStretch()  # Add a spacer item
        add_category_button = QPushButton("Add Category")
        add_category_button.clicked.connect(self.open_category_dialog)
        row3.addWidget(add_category_button)
        row3.addWidget(self.btn_add)
        
        ## Set the Master Layout
        master.addLayout(row1)
        master.addLayout(row2)
        master.addLayout(row3)
        master.addWidget(self.table)
        
        # Set the Final Layout
        self.setLayout(master)
        
    # Populate the Dropdown
    def populate_dropdown(self):
        self.dropdown.clear()
        categories = fetch_categories()
        for category in categories:
            self.dropdown.addItem(category[1], category[0])
    
    # Open the Category Dialog
    def open_category_dialog(self):
        dialog = CategoryDialog(self)
        dialog.finished.connect(self.populate_dropdown)
        dialog.exec()
    
    # Add an expense to the table
    def add_expense(self):
        date = self.date_box.date().toString(Qt.DateFormat.ISODate)
        category_id = self.dropdown.currentData()
        amount = self.amount.text()
        description = self.description.text()
        
        if not amount:
            QMessageBox.warning(self, "Warning", "Amount cannot be empty.")
            return
        
        try:
            amount = float(amount)
        except ValueError:
            QMessageBox.warning(self, "Warning", "Amount must be a number.")
            return
        
        if add_expense(date, category_id, amount, description):
            self.refresh_table()
        else:
            QMessageBox.critical(self, "Error", "Failed to add expense.")

    # Refresh the table with the latest data
    def refresh_table(self):
        self.table.setRowCount(0)
        expenses = fetch_expenses()
        print("Expenses fetched:", expenses)  # Debug statement
        for expense in expenses:
            print("Processing expense:", expense)  # Debug statement
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(str(expense[0])))
            self.table.setItem(row_position, 1, QTableWidgetItem(expense[1]))
            self.table.setItem(row_position, 2, QTableWidgetItem(expense[2]))
            try:
                amount = float(expense[3])
            except ValueError:
                amount = 0.0
            self.table.setItem(row_position, 3, QTableWidgetItem(f"${amount:.2f}"))
            self.table.setItem(row_position, 4, QTableWidgetItem(expense[4]))
            
            # Create the action buttons
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            btn_edit = QPushButton("Edit")
            btn_delete = QPushButton("Delete")
            
            action_layout.addWidget(btn_edit)
            action_layout.addWidget(btn_delete)
            action_layout.setContentsMargins(0, 0, 0, 0)
            action_widget.setLayout(action_layout)
            
            self.table.setCellWidget(row_position, 5, action_widget)
            
            # Connect the buttons to their respective functions
            btn_edit.clicked.connect(partial(self.edit_expense, row_position))
            btn_delete.clicked.connect(partial(self.delete_expense, row_position))

    # Edit an expense
    def edit_expense(self, row):
        expense_id = int(self.table.item(row, 0).text())
        dialog = EditExpenseDialog(expense_id, self)
        if dialog.exec():
            self.refresh_table()

    # Delete an expense
    def delete_expense(self, row):
        expense_id = int(self.table.item(row, 0).text())
        dialog = DeleteExpenseDialog(expense_id, self)
        if dialog.exec():
            self.refresh_table()

# Run the App
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = ExpenseApp()
    window.show()
    sys.exit(app.exec())