# create_db.py (выполните отдельно для создания базы данных)
import sqlite3

# Создаем базу данных
conn = sqlite3.connect('coffee.sqlite')
cursor = conn.cursor()

# Создаем таблицу
cursor.execute('''
CREATE TABLE IF NOT EXISTS coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roast_level TEXT NOT NULL,
    grind_type TEXT NOT NULL,
    taste_description TEXT,
    price REAL NOT NULL,
    package_volume INTEGER NOT NULL
)
''')

# Добавляем тестовые данные
test_data = [
    ('Эфиопия Сидамо', 'Светлая', 'В зернах', 'Цитрусовые нотки, ягодный аромат', 850, 250),
    ('Колумбия Супремо', 'Средняя', 'Молотый', 'Шоколад, орехи, карамель', 720, 200),
    ('Бразилия Сантос', 'Темная', 'В зернах', 'Шоколад, орехи, минимальная кислинка', 680, 300),
    ('Коста-Рика Тарразу', 'Средняя', 'В зернах', 'Фруктовый букет, мед, цитрус', 950, 250),
    ('Гватемала Антигуа', 'Средне-темная', 'Молотый', 'Какао, специи, дымные нотки', 890, 200),
    ('Кения АА', 'Светлая', 'В зернах', 'Ягодный, винный, сложный вкус', 1200, 250),
    ('Суматра Манделинг', 'Темная', 'В зернах', 'Пряный, травяной, полное тело', 780, 300),
    ('Йемен Мокко', 'Средняя', 'Молотый', 'Винный, шоколадный, с нотами сухофруктов', 1350, 200)
]

cursor.executemany('''
INSERT INTO coffee (name, roast_level, grind_type, taste_description, price, package_volume)
VALUES (?, ?, ?, ?, ?, ?)
''', test_data)

conn.commit()
conn.close()

print("База данных coffee.sqlite успешно создана!")