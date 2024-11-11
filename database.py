from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QMessageBox

def init_db(db_name):
    try:
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName(db_name)
        
        if not database.open():
            raise Exception("Database Error: {}".format(database.lastError().text()))
        
        #drop_tables()  # Drop existing tables
        if not create_tables():
            return False
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

#def drop_tables():
#      try:
#          query = QSqlQuery()
#          query.exec("DROP TABLE IF EXISTS expenses")
#          query.exec("DROP TABLE IF EXISTS categories")
#      except Exception as e:
#          QMessageBox.critical(None, "Error", str(e))

def create_tables():
    try:
        query = QSqlQuery()
        query.exec("""
                   CREATE TABLE IF NOT EXISTS categories 
                   (
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      name TEXT UNIQUE
                   )
                   """)
        if not query.isActive():
            raise Exception("Error in creating categories table: {}".format(query.lastError().text()))

        query.exec("""
                   CREATE TABLE IF NOT EXISTS expenses 
                   (
                      id INTEGER PRIMARY KEY AUTOINCREMENT, 
                      date TEXT, 
                      category_id INTEGER, 
                      amount NUMERIC(10, 2), 
                      description TEXT,
                      FOREIGN KEY (category_id) REFERENCES categories(id)
                   )
                   """)
        if not query.isActive():
            raise Exception("Error in creating expenses table: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Fetch all categories from the database
def fetch_categories():
    try:
        query = QSqlQuery()
        query.exec("SELECT * FROM categories ORDER BY name ASC")
        
        if not query.isActive():
            raise Exception("Error in fetching categories: {}".format(query.lastError().text()))
        
        categories = []
        while query.next():
            categories.append((query.value(0), query.value(1)))
        
        return categories
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return []

# Add a category to the database
def add_category(name):
    try:
        query = QSqlQuery()
        query.prepare("INSERT INTO categories (name) VALUES (:name)")
        query.bindValue(":name", name)
        
        if not query.exec():
            raise Exception("Error in adding category: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Update a category in the database
def update_category(id, name):
    try:
        query = QSqlQuery()
        query.prepare("UPDATE categories SET name = :name WHERE id = :id")
        query.bindValue(":name", name)
        query.bindValue(":id", id)
        
        if not query.exec():
            raise Exception("Error in updating category: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Delete a category from the database
def delete_category(id):
    try:
        query = QSqlQuery()
        query.prepare("DELETE FROM categories WHERE id = :id")
        query.bindValue(":id", id)
        
        if not query.exec():
            raise Exception("Error in deleting category: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Fetch all the data from the database
def fetch_expenses():
    try:
        query = QSqlQuery()
        query.exec("""
                   SELECT expenses.id, date, categories.name, amount, description
                   FROM expenses
                   JOIN categories ON expenses.category_id = categories.id
                   ORDER BY date DESC
                   """)
        
        if not query.isActive():
            raise Exception("Error in fetching data: {}".format(query.lastError().text()))
        
        expenses = []
        while query.next():
            expense = [query.value(i) for i in range(5)]
            print("Fetched expense:", expense)  # Debug statement
            expenses.append(expense)
        
        return expenses
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return []

# Add an expense to the database
def add_expense(date, category_id, amount, description):
    try:
        query = QSqlQuery()
        query.prepare("""
                      INSERT INTO expenses (date, category_id, amount, description)
                      VALUES (:date, :category_id, :amount, :description)
                      """)
        
        query.bindValue(":date", date)
        query.bindValue(":category_id", category_id)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        
        if not query.exec():
            raise Exception("Error in adding expense: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Update an expense in the database
def update_expense(id, date, category_id, amount, description):
    try:
        query = QSqlQuery()
        query.prepare("""
                      UPDATE expenses
                      SET date = :date, category_id = :category_id, amount = :amount, description = :description
                      WHERE id = :id
                      """)
        
        query.bindValue(":date", date)
        query.bindValue(":category_id", category_id)
        query.bindValue(":amount", amount)
        query.bindValue(":description", description)
        query.bindValue(":id", id)
        
        if not query.exec():
            raise Exception("Error in updating expense: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False

# Delete an expense from the database
def delete_expense(id):
    try:
        query = QSqlQuery()
        query.prepare("DELETE FROM expenses WHERE id = :id")
        query.bindValue(":id", id)
        
        if not query.exec():
            raise Exception("Error in deleting expense: {}".format(query.lastError().text()))
        
        return True
    except Exception as e:
        QMessageBox.critical(None, "Error", str(e))
        return False