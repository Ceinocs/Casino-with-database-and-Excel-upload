import sqlite3

import self

connection = sqlite3.connect('practic.db')
cursor = connection.cursor()

# 1. Создаем таблицу (если её нет)
cursor.execute('''
CREATE TABLE IF NOT EXISTS players (
    score INTEGER DEFAULT 100
)
''')
connection.commit()

# 2. ДОБАВЛЯЕМ СТРОКУ (иначе таблица будет пустой и читать нечего)
# Запишем пустую строку, чтобы сработало значение по умолчанию (100)
cursor.execute("INSERT INTO players DEFAULT VALUES")
connection.commit()

# 3. ДЕЛАЕМ ЗАПРОС НА ПОЛУЧЕНИЕ
cursor.execute("SELECT score FROM players")

# 4. СОХРАНЯЕМ В ПЕРЕМЕННУЮ PYTHON
row = cursor.fetchone() # fetchone() возвращает кортеж, например: (100,)

if row is not None:
    my_score = row[0]   # Извлекаем само число из кортежа по индексу 0
    print(f"Значение переменной score в Python: {my_score}")
else:
    print("Таблица пустая!")

cursor.close()
connection.close()

#67
try:
    # ИСПРАВЛЕНО: передаем ID, Имя, Баланс 1000 и Профит 0 в правильном порядке
    cursor.execute(
        "INSERT INTO users (user_name, balance, profit) VALUES ( ?, 1000, 0)",
        (User_name)
    )
    connection.commit()
    print(
        f"Вы успешно зарегистрированы!\n"
        f"Добро пожаловать, {User_name} 🎉🎉🎉"
    )

    # ИСПРАВЛЕНО: Вызываем экспорт с правильным именем метода expotr_to_excel
    self.expotr_to_excel()

    # ИСПРАВЛЕНО: Сохраняем баланс для отображения в меню
    self.result = [1000]
    self.game_menu()

except sqlite3.IntegrityError:
    print(
        f"🛑 Ошибка: Пользователь с именем '{User_name}' уже существует!"
    )
    print('Войдите в аккаунт')
    self.start()

finally:
    connection.close()
