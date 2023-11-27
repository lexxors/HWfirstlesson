import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = loadUi('main.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Coffee Information')
        self.load_data()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
