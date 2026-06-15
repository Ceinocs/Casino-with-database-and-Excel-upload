
from openpyxl import Workbook, load_workbook
import random
import sqlite3


class AppMenu:

    def database(self):
        # Оставляем имя базы данных
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Создаем таблицу пользователей, если её еще нет
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_name TEXT NOT NULL UNIQUE,
                balance INTEGER  DEFAULT 1000,
                profit INTEGER  DEFAULT 0
            )
        """
        )
        connection.commit()
        connection.close()

    def export_to_excel(self):
        # ИСПРАВЛЕНО: Добавлено создание книги Workbook и cursor для SQL
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT user_name, balance, profit FROM users")
        rows = cursor.fetchall()

        wb = Workbook()
        ws = wb.active
        ws.title = "Пользователи"

        # Записываем шапку
        ws.append(["User_Name", "Balance", "Profit"])

        # Записываем все строки из SQL
        for row in rows:
            ws.append(row)

        wb.save("database.xlsx")
        connection.close()

    # Регистрация
    def register(self):
        print('\nУкажите логин: ')
        user_name = str(input())

        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT user_name FROM users WHERE user_name = ?", (user_name,))
        result = cursor.fetchone()

        if result is None:
            cursor.execute("INSERT INTO users (User_name) VALUES (?)", (user_name,))
            connection.commit()
            connection.close()

            self.user_name = user_name

            print(f"\nДобро пожаловать {user_name}")
            self.game_menu()
        else:
            connection.close()
            print(f"\nЛогин: '{user_name}' уже занято. Придумайте новое или войдите")
            self.main_menu()

        #67

    # Вход
    def entrance(self):
        print('\nВведите имя: ')
        user_name = str(input())

        # Подключаемся к SQL для поиска пользователя
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute("SELECT balance FROM users WHERE user_name = ?", (user_name,))
        self.result = cursor.fetchone()
        connection.close()

        if self.result is not None:
            self.User_name = user_name
            print(f'\nВы успешно вошли! С возвращением, {user_name}!')
            self.game_menu()
        else:
            print('\nПользователь с таким именем не найден!')
            print('\nВернуться назад?')
            end = int(input('1 - Да / 2 - Нет? '))
            if end == 1:
                self.register()  # ИСПРАВЛЕНО: Использование self.start() вместо app.start()



    def overflow(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        print('Введие сумму пополнения: ')

        profit = int(input('Ваша сумма: '))

        # Прибавляем к profit
        cursor.execute(
            "UPDATE users SET profit = profit + ? WHERE user_name = ?",
            (profit, self.user_name)
        )
        connection.commit()

        # Прибовляем к balance
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_name = ?",
            (profit, self.user_name)
        )

        connection.commit()

        # cursor.execute("SELECT balance FROM users WHERE user_name = ?", (self.User_name,))
        #
        # data = cursor.fetchone()  # Забираем результат (вернет кортеж)
        #
        # print("\nБланас успешно пополнен!"
        #       f"\n Ваш баланс теперь {data[0]}")

        self.game_menu()

        cursor.close()
        connection.close()

    def game_menu(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute("SELECT balance FROM users WHERE user_name = ?", (self.user_name,))

        data = cursor.fetchone()  # Забираем результат (вернет кортеж)

        print(
            f'\nВаш баланс {data[0]} рублей'
            '\n1 крутить рулетку'
            '\n2 по полнить баланс'
            '\n3 Выйти')
        choice = int(input('Выберите: '))

        if choice == 1:
            self.cheak()
        if choice == 2:
            self.overflow()
        else:
            exit()

        cursor.close()
        connection.close()

    def cheak(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # проверка на сумму

        cursor.execute("SELECT balance FROM users WHERE user_name = ?", (self.user_name,))

        data = cursor.fetchone()  # Забираем результат (вернет кортеж)

        if data[0] >= 30:
            self.game()
        else:
            print(f'\n У вас не достаточно средств'
                  f'\n 1 - По полнить'
                  f'\n 2 - меню')
            choice = int(input('Ваш выбор: '))
            if choice == 1:
                self.overflow()
            else:
                self.game_menu()
    def game(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        # Отнимание денежег хихихи

        profit_to_sub = 30

        # забираем 30 очков
        cursor.execute(
            "UPDATE users SET balance = balance - ? WHERE user_name = ?",
            (profit_to_sub, self.user_name)
        )
        connection.commit()



        simvols = ['🍒', '🍋', '🍇']

        item = simvols[random.randint(0, 2)]
        item_2 = simvols[random.randint(0, 2)]
        item_3 = simvols[random.randint(0, 2)]

        point_to_add = 0

        if (item == item_2 == item_3 == '🍒'):
            point_to_add = 20
        if (item == item_2 == item_3 == '🍋'):
            point_to_add = 40
        if (item == item_2 == item_3 == '🍇'):
            point_to_add = 80

        # прибовляет очки
        cursor.execute(
            "UPDATE users SET balance = balance + ? WHERE user_name = ?",
            (point_to_add, self.user_name)
        )

        connection.commit()

        # отнимаем profit
        cursor.execute(
            "UPDATE users SET profit = profit - ? WHERE user_name = ?",
            (point_to_add, self.user_name)
        )
        connection.commit()

        cursor.execute("SELECT balance FROM users WHERE user_name = ?", (self.user_name,))

        data = cursor.fetchone()  # Забираем результат (вернет кортеж)

        cursor.close()
        connection.close()

        print(
            f'\n{item} {item_2} {item_3}'
            f'\n Ваш выйграшь {point_to_add} рублей.'
            f'\nВаш баланс {data[0]}'
            f'\n 1 крутить еще'
            f'\n 2 В меню')

        choice = int(input('Ваш выбор: '))

        if choice == 1:
            self.cheak()
        else:
            self.game_menu()


    # Старт
    def main_menu(self):
        self.database()
        self.export_to_excel()
        print(
            '\n_________Добро пожаловать в КАЗИНО 777_________'
            '\n1 Зарегистрироваться'
            '\n2 Войти'
            '\n3 Выйти'
        )
        choice = int(input('Выберите: '))
        if choice == 1:
            self.register()
        if choice == 2:
            self.entrance()
        else:
            exit()


if __name__ == "__main__":
    app = AppMenu()  # Создаем объект нашего меню
    app.main_menu()
