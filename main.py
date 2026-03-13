import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.uic import loadUi
from add_edit_form import AddEditCoffeeForm


class CoffeeInfoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)

        # Настройка таблицы
        self.coffeeTable.setColumnCount(7)
        self.coffeeTable.setHorizontalHeaderLabels([
            'ID', 'Название сорта', 'Степень обжарки',
            'Молотый/В зернах', 'Описание вкуса',
            'Цена (руб)', 'Объем упаковки (г)'
        ])

        # Подключение кнопок
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

        # Автоматическая загрузка данных при запуске
        self.load_data()

    def load_data(self):
        """Загрузка данных из базы данных"""
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

    def add_coffee(self):
        """Добавление новой записи"""
        form = AddEditCoffeeForm(self)
        if form.exec():
            data = form.get_data()
            if data:
                try:
                    conn = sqlite3.connect('coffee.sqlite')
                    cursor = conn.cursor()

                    cursor.execute('''
                        INSERT INTO coffee 
                        (name, roast_level, grind_type, taste_description, price, package_volume)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        data['name'], data['roast_level'], data['grind_type'],
                        data['taste_description'], data['price'], data['package_volume']
                    ))

                    conn.commit()
                    conn.close()

                    self.load_data()
                    QMessageBox.information(self, "Успех", "Запись успешно добавлена")

                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")

    def edit_coffee(self):
        """Редактирование выбранной записи"""
        current_row = self.coffeeTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")
            return

        # Получаем ID выбранной записи
        coffee_id = int(self.coffeeTable.item(current_row, 0).text())

        try:
            conn = sqlite3.connect('coffee.sqlite')
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM coffee WHERE id = ?', (coffee_id,))
            coffee_data = cursor.fetchone()
            conn.close()

            if coffee_data:
                form = AddEditCoffeeForm(self, coffee_data)
                if form.exec():
                    data = form.get_data()
                    if data:
                        try:
                            conn = sqlite3.connect('coffee.sqlite')
                            cursor = conn.cursor()

                            cursor.execute('''
                                UPDATE coffee 
                                SET name = ?, roast_level = ?, grind_type = ?,
                                    taste_description = ?, price = ?, package_volume = ?
                                WHERE id = ?
                            ''', (
                                data['name'], data['roast_level'], data['grind_type'],
                                data['taste_description'], data['price'],
                                data['package_volume'], coffee_id
                            ))

                            conn.commit()
                            conn.close()

                            self.load_data()
                            QMessageBox.information(self, "Успех", "Запись успешно обновлена")

                        except sqlite3.Error as e:
                            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка базы данных: {e}")


def main():
    app = QApplication(sys.argv)
    window = CoffeeInfoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()