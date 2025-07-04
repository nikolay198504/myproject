import sqlite3

conn = sqlite3.connect('orders.db')
cursor = conn.cursor()

# Добавить поле type, если его нет
try:
    cursor.execute("ALTER TABLE orders ADD COLUMN type TEXT DEFAULT 'personal';")
    print("Поле type успешно добавлено!")
except Exception as e:
    print("Ошибка или поле уже существует:", e)

conn.commit()
conn.close() 