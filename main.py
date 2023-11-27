import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QDialog, QMessageBox
from PyQt5.uic import loadUi
import sqlite3
from add_edit_coffee_form import AddEditCoffeeForm


class CoffeeApp(QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()

        self.ui = loadUi('main.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Coffee Information')

        self.load_data()

        self.ui.addButton.clicked.connect(self.add_coffee)
        self.ui.editButton.clicked.connect(self.edit_coffee)

    def load_data(self):
        try:
            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM coffee")
            data = cursor.fetchall()

            self.ui.tableWidget.setRowCount(len(data))
            self.ui.tableWidget.setColumnCount(len(data[0]))

            for i, row in enumerate(data):
                for j, item in enumerate(row):
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))

            connection.close()
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def add_coffee(self):
        form = AddEditCoffeeForm()
        if form.exec_() == QDialog.Accepted:
            coffee_data = form.save_data()
            self.save_to_database(coffee_data)
            self.load_data()

    def edit_coffee(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row != -1:
            coffee_data = {
                'id': int(self.ui.tableWidget.item(selected_row, 0).text()),
                'name': self.ui.tableWidget.item(selected_row, 1).text(),
                'roast_degree': self.ui.tableWidget.item(selected_row, 2).text(),
                'ground_or_whole': self.ui.tableWidget.item(selected_row, 3).text(),
                'flavor_description': self.ui.tableWidget.item(selected_row, 4).text(),
                'price': float(self.ui.tableWidget.item(selected_row, 5).text()),
                'package_volume': int(self.ui.tableWidget.item(selected_row, 6).text())
            }

            form = AddEditCoffeeForm(coffee_data)
            if form.exec_() == QDialog.Accepted:
                updated_data = form.save_data()
                self.update_database(updated_data)
                self.load_data()
        else:
            QMessageBox.warning(self, 'Warning', 'Please select a coffee to edit.')

    def save_to_database(self, coffee_data):
        try:
            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()

            cursor.execute('''
                INSERT INTO coffee (name, roast_degree, ground_or_whole, flavor_description, price, package_volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                coffee_data['name'],
                coffee_data['roast_degree'],
                coffee_data['ground_or_whole'],
                coffee_data['flavor_description'],
                coffee_data['price'],
                coffee_data['package_volume']
            ))

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Database error: {e}')

    def update_database(self, coffee_data):
        try:
            connection = sqlite3.connect('coffee.sqlite')
            cursor = connection.cursor()

            cursor.execute('''
                UPDATE coffee
                SET name=?, roast_degree=?, ground_or_whole=?, flavor_description=?, price=?, package_volume=?
                WHERE id=?
            ''', (
                coffee_data['name'],
                coffee_data['roast_degree'],
                coffee_data['ground_or_whole'],
                coffee_data['flavor_description'],
                coffee_data['price'],
                coffee_data['package_volume'],
                coffee_data['id']
            ))

            connection.commit()
            connection.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Error', f'Database error: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
