import sys
import os
from PyQt6.QtWidgets import QDialog, QMessageBox

try:
    from addEditCoffeeForm_ui import Ui_AddEditCoffeeForm
except ImportError:
    import importlib.util

    ui_path = os.path.join(os.path.dirname(__file__), 'addEditCoffeeForm_ui.py')
    spec = importlib.util.spec_from_file_location("addEditCoffeeForm_ui", ui_path)
    addEditCoffeeForm_ui = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(addEditCoffeeForm_ui)
    Ui_AddEditCoffeeForm = addEditCoffeeForm_ui.Ui_AddEditCoffeeForm


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None, coffee_data=None):
        super().__init__(parent)
        self.setupUi(self)

        if coffee_data:
            self.setWindowTitle("Редактирование кофе")
            self.coffee_id = coffee_data[0]
            self.nameEdit.setText(coffee_data[1])

            index = self.roastCombo.findText(coffee_data[2])
            if index >= 0:
                self.roastCombo.setCurrentIndex(index)

            index = self.grindCombo.findText(coffee_data[3])
            if index >= 0:
                self.grindCombo.setCurrentIndex(index)

            self.tasteEdit.setText(coffee_data[4])
            self.priceSpin.setValue(float(coffee_data[5]))
            self.volumeSpin.setValue(int(coffee_data[6]))
        else:
            self.setWindowTitle("Добавление кофе")
            self.coffee_id = None

        self.saveButton.clicked.connect(self.save_data)
        self.cancelButton.clicked.connect(self.reject)

    def save_data(self):
        if not self.nameEdit.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название сорта")
            return

        if self.priceSpin.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть больше 0")
            return

        self.result_data = {
            'id': self.coffee_id,
            'name': self.nameEdit.text().strip(),
            'roast_level': self.roastCombo.currentText(),
            'grind_type': self.grindCombo.currentText(),
            'taste_description': self.tasteEdit.toPlainText().strip(),
            'price': self.priceSpin.value(),
            'package_volume': self.volumeSpin.value()
        }

        self.accept()

    def get_data(self):
        return getattr(self, 'result_data', None)