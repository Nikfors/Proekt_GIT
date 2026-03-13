import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt6.uic import loadUi


class CoffeeInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.coffeeTable.setColumnCount(7)
        self.coffeeTable.setHorizontalHeaderLabels([
            'ID', 'Название сорта', 'Степень обжарки',
            'Молотый/В зернах', 'Описание вкуса',
            'Цена (руб)', 'Объем упаковки (г)'
        ])
        self.load_data()

    def load_data(self):
        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM coffee ORDER BY id')
            data = cursor.fetchall()
            self.coffeeTable.setRowCount(0)

            for row_idx, row_data in enumerate(data):
                self.coffeeTable.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    if col_idx == 5:  # Цена
                        item = QTableWidgetItem(f"{value:.2f}")
                    else:
                        item = QTableWidgetItem(str(value))
                    self.coffeeTable.setItem(row_idx, col_idx, item)
            self.coffeeTable.resizeColumnsToContents()
            self.statusbar.showMessage(f"Загружено {len(data)} записей")
            conn.close()

        except sqlite3.Error as e:
            self.statusbar.showMessage(f"Ошибка базы данных: {e}")
        except FileNotFoundError:
            self.statusbar.showMessage("Файл базы данных не найден")


def main():
    app = QApplication(sys.argv)
    window = CoffeeInfoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()