from PyQt6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QListWidget
from database import fetch_categories, add_category, update_category, delete_category

class CategoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Manage Categories")
        self.setGeometry(800, 400, 400, 300)
        self.selected_category_id = None  # Initialize selected_category_id
        self.initUI()
        self.load_categories()

    def initUI(self):
        layout = QVBoxLayout()

        self.category_list = QListWidget()
        self.category_list.itemClicked.connect(self.on_category_selected)
        layout.addWidget(self.category_list)

        self.name_edit = QLineEdit()
        layout.addWidget(QLabel("Category Name:"))
        layout.addWidget(self.name_edit)

        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add")
        self.update_button = QPushButton("Update")
        self.delete_button = QPushButton("Delete")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.add_button.clicked.connect(self.add_category)
        self.update_button.clicked.connect(self.update_category)
        self.delete_button.clicked.connect(self.delete_category)
        self.cancel_button.clicked.connect(self.reject)

    def load_categories(self):
        self.category_list.clear()
        categories = fetch_categories()
        for category in categories:
            self.category_list.addItem(f"{category[0]}: {category[1]}")

    def on_category_selected(self, item):
        category_id, category_name = item.text().split(": ")
        self.selected_category_id = int(category_id)
        self.name_edit.setText(category_name)

    def add_category(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
            return

        if add_category(name):
            self.load_categories()
            self.name_edit.clear()
        else:
            QMessageBox.critical(self, "Error", "Failed to add category.")

    def update_category(self):
        if self.selected_category_id is None:
            QMessageBox.warning(self, "Warning", "No category selected.")
            return

        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Category name cannot be empty.")
            return

        if update_category(self.selected_category_id, name):
            self.load_categories()
            self.name_edit.clear()
            self.selected_category_id = None  # Reset selected_category_id
        else:
            QMessageBox.critical(self, "Error", "Failed to update category.")

    def delete_category(self):
        if self.selected_category_id is None:
            QMessageBox.warning(self, "Warning", "No category selected.")
            return

        if delete_category(self.selected_category_id):
            self.load_categories()
            self.name_edit.clear()
            self.selected_category_id = None  # Reset selected_category_id
        else:
            QMessageBox.critical(self, "Error", "Failed to delete category.")

# Example usage
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    dialog = CategoryDialog()
    dialog.exec()