import os
import subprocess
import shutil


def convert_ui_to_py():
    print("Конвертация UI файлов...")

    subprocess.run([
        'pyuic6',
        '-x',
        'UI/main.ui',
        '-o',
        'UI/main_ui.py'
    ], check=True)

    subprocess.run([
        'pyuic6',
        '-x',
        'UI/addEditCoffeeForm.ui',
        '-o',
        'UI/addEditCoffeeForm_ui.py'
    ], check=True)

    shutil.copy2('UI/main_ui.py', 'main_ui.py')
    shutil.copy2('UI/addEditCoffeeForm_ui.py', 'addEditCoffeeForm_ui.py')

    print("Готово! Файлы созданы в папке UI и скопированы в корень:")


if __name__ == "__main__":
    convert_ui_to_py()