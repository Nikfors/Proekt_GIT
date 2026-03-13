import os
import shutil
import subprocess
import PyInstaller.__main__


def build_executable():
    print("=" * 50)
    print("СБОРКА ПРИЛОЖЕНИЯ Coffee App")
    print("=" * 50)

    print("\n1. Конвертация UI файлов в PY...")
    os.makedirs('UI', exist_ok=True)

    subprocess.run(['pyuic6', '-x', 'UI/main.ui', '-o', 'UI/main_ui.py'], check=True)
    subprocess.run(['pyuic6', '-x', 'UI/addEditCoffeeForm.ui', '-o', 'UI/addEditCoffeeForm_ui.py'], check=True)
    print("   UI файлы сконвертированы")

    print("\n2. Подготовка папки release...")
    if os.path.exists('release'):
        shutil.rmtree('release')
    os.makedirs('release', exist_ok=True)

    print("   Копирование файлов в корень release...")

    shutil.copy2('UI/main_ui.py', 'release/main_ui.py')
    shutil.copy2('UI/addEditCoffeeForm_ui.py', 'release/addEditCoffeeForm_ui.py')

    if os.path.exists('data/coffee.sqlite'):
        shutil.copy2('data/coffee.sqlite', 'release/coffee.sqlite')
        print(f"   База данных скопирована: data/coffee.sqlite -> release/coffee.sqlite")
    else:
        print("   ВНИМАНИЕ: Файл data/coffee.sqlite не найден!")

    shutil.copy2('main.py', 'release/main.py')
    shutil.copy2('add_edit_form.py', 'release/add_edit_form.py')

    with open('release/README.txt', 'w', encoding='utf-8') as f:
        f.write('''ПРОГРАММА "ИНФОРМАЦИЯ О КОФЕ"
===========================

Файлы в папке:
- coffee_app.exe - исполняемый файл
- coffee.sqlite - база данных
- main_ui.py - интерфейс главного окна
- addEditCoffeeForm_ui.py - интерфейс формы
- main.py - код программы
- add_edit_form.py - код формы

Запуск:
- Просто запустите coffee_app.exe
''')

    with open('release/requirements.txt', 'w', encoding='utf-8') as f:
        f.write('PyQt6==6.4.2\n')
    print("\n3. Сборка исполняемого файла coffee_app.exe...")
    os.makedirs('build_temp', exist_ok=True)

    shutil.copy2('main.py', 'build_temp/main.py')
    shutil.copy2('add_edit_form.py', 'build_temp/add_edit_form.py')
    shutil.copy2('UI/main_ui.py', 'build_temp/main_ui.py')
    shutil.copy2('UI/addEditCoffeeForm_ui.py', 'build_temp/addEditCoffeeForm_ui.py')

    os.chdir('build_temp')

    # Собираем exe
    PyInstaller.__main__.run([
        'main.py',
        '--name=coffee_app',
        '--onefile',
        '--windowed',
        '--add-data=main_ui.py;.',
        '--add-data=addEditCoffeeForm_ui.py;.',
        '--hidden-import=add_edit_form',
        '--hidden-import=PyQt6',
        '--hidden-import=sqlite3',
        '--distpath=../release',
        '--workpath=build',
        '--specpath=.',
        '--clean'
    ])

    os.chdir('..')

    print("\n4. Очистка временных файлов...")
    if os.path.exists('build_temp'):
        shutil.rmtree('build_temp')

    print("\n" + "=" * 50)
    print("СБОРКА ЗАВЕРШЕНА УСПЕШНО!")
    print("=" * 50)
    print("\nПапка release содержит:")
    files = os.listdir('release')
    for f in sorted(files):
        size = os.path.getsize(os.path.join('release', f))
        print(f"  - {f} ({size / 1024:.1f} KB)")
    print("\nГотово! Все файлы в корне папки release/")


if __name__ == "__main__":
    build_executable()