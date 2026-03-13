import sys
import os
import sqlite3
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox

# Импортируем UI файлы (они теперь в той же папке)
try:
    from main_ui import Ui_MainWindow
except ImportError:
    # Если не получается, ищем в текущей папке
    import importlib.util

    ui_path = os.path.join(os.path.dirname(__file__), 'main_ui.py')
    spec = importlib.util.spec_from_file_location("main_ui", ui_path)
    main_ui = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(main_ui)
    Ui_MainWindow = main_ui.Ui_MainWindow

from add_edit_form import AddEditCoffeeForm


class CoffeeInfoApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Определяем путь к базе данных (просто в той же папке)
        self.db_path = self.get_database_path()
        print(f"Путь к базе данных: {self.db_path}")

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

        # Загрузка данных
        self.load_data()

    def get_database_path(self):
        """Возвращает путь к базе данных (в той же папке, что и программа)"""
        if getattr(sys, 'frozen', False):
            # Запуск из exe
            base_path = os.path.dirname(sys.executable)
        else:
            # Запуск из скрипта
            base_path = os.path.dirname(os.path.abspath(__file__))

        # База данных просто в корне, рядом с exe
        return os.path.join(base_path, 'coffee.sqlite')

    def load_data(self):
        """Загрузка данных из базы данных"""
        try:
            if not os.path.exists(self.db_path):
                self.statusbar.showMessage(f"База данных не найдена: {self.db_path}")
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coffee'")
            if not cursor.fetchone():
                self.statusbar.showMessage("Таблица coffee не найдена")
                conn.close()
                return

            cursor.execute('SELECT * FROM coffee ORDER BY id')
            data = cursor.fetchall()

            self.coffeeTable.setRowCount(0)

            for row_idx, row_data in enumerate(data):
                self.coffeeTable.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    if col_idx == 5:
                        item = QTableWidgetItem(f"{value:.2f}")
                    else:
                        item = QTableWidgetItem(str(value))
                    self.coffeeTable.setItem(row_idx, col_idx, item)

            self.coffeeTable.resizeColumnsToContents()
            self.statusbar.showMessage(f"Загружено {len(data)} записей")
            conn.close()

        except Exception as e:
            self.statusbar.showMessage(f"Ошибка: {e}")

    def add_coffee(self):
        """Добавление новой записи"""
        form = AddEditCoffeeForm(self)
        if form.exec():
            data = form.get_data()
            if data:
                try:
                    conn = sqlite3.connect(self.db_path)
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

                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")

    def edit_coffee(self):
        """Редактирование выбранной записи"""
        current_row = self.coffeeTable.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для редактирования")
            return

        coffee_id = int(self.coffeeTable.item(current_row, 0).text())

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM coffee WHERE id = ?', (coffee_id,))
            coffee_data = cursor.fetchone()
            conn.close()

            if coffee_data:
                form = AddEditCoffeeForm(self, coffee_data)
                if form.exec():
                    data = form.get_data()
                    if data:
                        conn = sqlite3.connect(self.db_path)
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

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")


def main():
    app = QApplication(sys.argv)
    window = CoffeeInfoApp()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()