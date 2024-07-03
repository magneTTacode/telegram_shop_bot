from aiogram import F, Router, types
from aiogram import Bot
import aiogram.utils
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import io
from aiogram.types import InputFile
import uuid
import mysql.connector
import config
import pandas as pd
from aiogram.types import FSInputFile
from datetime import datetime

import kb
import text
import db
import config

bot = Bot(token=config.BOT_TOKEN)

async def send_menu_by_role(user_id: int):
    role = db.get_user_role(user_id)
    if role == 1:
        await send_user_menu(user_id)
    elif role == 2:
        await send_agent_menu(user_id)
    elif role == 3:
        await send_admin_menu(user_id)
    elif role == 4:
        await send_main_menu(user_id)
    else:
        print(f"Unknown role for user {user_id}")

async def send_main_menu(user_id):
    await bot.send_message(user_id, 'Панель главного администратора', reply_markup=kb.main_admin_kb)

async def send_user_menu(user_id: int):
    # Отправка меню для обычного пользователя
    await bot.send_message(user_id, "Меню", reply_markup=kb.user_keyboard)

async def send_agent_menu(user_id: int):
    # Отправка меню для агента
    await bot.send_message(user_id, "Меню", reply_markup=kb.agent_keyboard)

async def send_admin_menu(user_id: int):
    # Отправка меню для админа (если необходимо)
    await bot.send_message(user_id, "Админ панель", kb.admin_kb)

db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'wFaEPSogZvh94bfu',
    'database': "tgbot"
}

async def send_user_profile(user_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch balance and subscription_end from profiles for the given user_id
        cursor.execute("SELECT balance, subscription_end FROM profiles WHERE user_id = %s", (user_id,))
        profile_data = cursor.fetchone()

        if profile_data:
            # Format message text in Russian
            if profile_data['subscription_end']:
                subscription_status = f"⏳ Подписка действительна до: {profile_data['subscription_end'].strftime('%d.%m.%Y')}"
            else:
                subscription_status = "⚠️ У вас нет активной подписки"

            message_text = f"Ваш профиль:\n\n"
            message_text += subscription_status + "\n"
            message_text += f"💰 Остаток на балансе: {profile_data['balance']}"

            # Send message with keyboard
            await bot.send_message(user_id, message_text, reply_markup=kb.profile_keyboard)
            print(f"Сообщение отправлено пользователю с user_id={user_id}")
            return True
        else:
            print(f"Не удалось отправить сообщение, профиль пользователя с user_id={user_id} не найден.")
            return False

    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return False

    finally:
        # Close database connection
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def send_category_message(chat_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Получаем все имена категорий
        cursor.execute("SELECT name FROM categories")
        categories = cursor.fetchall()
        buttons = [
    [KeyboardButton(text="обратно в меню")],  # First row with a single button
]
        clean_categories = [category[0] for category in categories]
        for c in clean_categories:
            buttons.append([KeyboardButton(text=c)])  # Wrap each button in a list

        # Создаем клавиатуру
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, keyboard=buttons)  


        await bot.send_message(chat_id=chat_id, text='Выберите категорию:', reply_markup=keyboard)

    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def send_first_product_with_image(chat_id: int, data, state):
    category_name = data['category']
    num = data['num']
    products = db.get_products_by_category(category_name)
    
    if len(products) == 0:
        await bot.send_message(chat_id=chat_id, text='Категория пуста.')
        await state.clear()
        await send_menu_by_role(chat_id)
    else:

        product = products[num]
        await state.update_data(prod_id = product[0])
        image_file = product[8]

        # image_file = 'AgACAgIAAxkBAAILQGZ-n6vA0xgSOryC1748uDnHX1u_AAIN3jEbGK74S2oJkdjpCZtCAQADAgADeAADNQQ'
        # Отправка сообщения с изображением
        if num == 0:
            if len(products) == 1:
                keyboard = kb.shop_kb_4
            else:
                keyboard = kb.shop_kb_1
        elif num+1 == len(products):
            if len(products) == 1:
                keyboard = kb.shop_kb_4
            else:
                keyboard = kb.shop_kb_3
        else:
            keyboard = kb.shop_kb_2
        if product[6] == 1:
            prod_6 = 'в наличии'
        else:
            prod_6 = 'нет в наличии'
        await bot.send_photo(chat_id, image_file, caption=f"{product[2]}\n\n"
                                                            f"Характеристика: {product[3]}\n\n"
                                                            f"Описание: {product[4]}\n\n"
                                                            f"Стоимость: {product[5]}, {prod_6}\n"
                                                            f"Срок доставки: {product[7]}\n\n"
                                                            f"{num+1} из {len(products)}", reply_markup=keyboard)
    
async def update_data_num(inf, state):
    data = await state.get_data()
    if inf == 'next_prod':
        data1 = data['num']
        data1 += 1
        await state.update_data(num = data1)
    elif inf == 'prev_prod':
        data1 = data['num']
        data1 -= 1
        await state.update_data(num = data1)
    elif inf == 'next_rev':
        data1 = data['rev_num']
        data1 += 1
        await state.update_data(rev_num = data1)
    elif inf == 'prev_rev':
        data1 = data['rev_num']
        data1 -= 1
        await state.update_data(rev_num = data1)

async def review_opt(chat_id, state):
    data = await state.get_data()
    review = data['review']
    await bot.send_message(chat_id=chat_id, text=f'Ваш отзыв:\n\n{review}', reply_markup=kb.rev_kb_wr_2)

async def add_review(state):
    data = await state.get_data()
    username = data['username']
    user_id = data['user_id']
    review_text = data['review']
    positive = data['positive']
    product_id = data['prod_id']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # SQL-запрос для вставки данных
        query = """
        INSERT INTO reviews (username, user_id, review_text, positive, product_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (username, user_id, review_text, positive, product_id)
        
        # Выполнение запроса
        cursor.execute(query, values)
        conn.commit()
        print("Отзыв добавлен успешно.")
        await bot.send_message(chat_id=user_id, text='Отзыв добавлен успешно.')
        
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        await bot.send_message(chat_id=user_id, text='Ошибка при добавлении отзыва.')
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        print("Соединение с базой данных закрыто.")

async def send_first_review(chat_id: int, state):
    data = await state.get_data()
    product_id = data['prod_id']
    rev_num = data['rev_num']

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Запрос для получения всех отзывов по product_id
        query = "SELECT * FROM reviews WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        reviews = cursor.fetchall()

        if rev_num == 0:
            if len(reviews) == 1:
                keyboard = kb.rev_kb_4
            else:
                keyboard = kb.rev_kb_1
        elif rev_num+1 == len(reviews):
            if len(reviews) == 1:
                keyboard = kb.rev_kb_4
            else:
                keyboard = kb.rev_kb_3
        else:
            keyboard = kb.rev_kb_2
        
        # Если есть отзывы, отправляем первый
        if reviews:
            first_review = reviews[rev_num]
            review_text = (f"Пользователь: {first_review[1]}\n"
                           f"ID пользователя: {first_review[2]}\n"
                           f"Отзыв: {first_review[3]}\n"
                           f"Положительный: {'Да' if first_review[4] else 'Нет'}\n"
                           f"ID продукта: {first_review[5]}")
            review_text = (f"{'Положительный' if first_review[4] else 'Отрицательный'} отзыв от пользователя {first_review[1]}\n\n"
                           f"{first_review[3]}\n\n"
                           f"{rev_num+1} из {len(reviews)}")
            await bot.send_message(chat_id=chat_id, text=review_text, reply_markup=keyboard)
        else:
            await bot.send_message(chat_id=chat_id, text="Отзывов для данного продукта нет.")
    
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
    
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
        print("Соединение с базой данных закрыто.")

async def add_admin(chat_id, state):
    data = await state.get_data()
    username = data['name']
    role = data['role']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Поиск user_id по username
        cursor.execute("SELECT chat_id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if user_id is None:
            await bot.send_message(chat_id, f"Пользователь с ником {username} не найден.")
            return

        user_id = user_id[0]

        # SQL-запрос для вставки данных
        query = "INSERT INTO admin (user_id, role) VALUES (%s, %s)"
        values = (user_id, role)

        # Выполнение запроса
        cursor.execute(query, values)
        conn.commit()

        await bot.send_message(chat_id, "Администратор добавлен успешно.")

    except:
        await bot.send_message(chat_id, f"Ошибка базы данных")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")

async def delete_admin(chat_id, state):
    data = await state.get_data()
    username = data['name']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Поиск user_id по username
        cursor.execute("SELECT chat_id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()

        if user_id is None:
            await bot.send_message(chat_id, f"Пользователь с ником {username} не найден.")
            return

        user_id = user_id[0]

        # SQL-запрос для удаления данных
        query = "DELETE FROM admin WHERE user_id = %s"
        values = (user_id,)

        # Выполнение запроса
        cursor.execute(query, values)
        conn.commit()

        if cursor.rowcount > 0:
            await bot.send_message(chat_id, "Администратор удален успешно.")
        else:
            await bot.send_message(chat_id, f"Администратор с ником {username} не найден.")

    except:
        await bot.send_message(chat_id, f"Ошибка базы данных")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")

def generate_invite_code():
    return str(uuid.uuid4())

# Функция для создания и сохранения ссылки приглашения
async def create_invite_link(state, chat_id):
    data = await state.get_data()
    user_name = data['name']
    user_id = get_user_id_by_username(user_name)
    invite_code = generate_invite_code()
    # invite_link = f"https://t.me/dark_c0d3_bot?start={invite_code}"
    
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Сохранение данных в таблице agents
        query = "INSERT INTO agents (user_id, invite_code, invited_users, earnings) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, invite_code, 0, 0.00))
        conn.commit()
        await bot.send_message(chat_id, text='Агент успешно добавлен.')
        
    except mysql.connector.Error as err:
        await bot.send_message(f"Ошибка базы данных: {err}")
        return None
    
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")
    
    # return invite_link

def get_user_id_by_username(username):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Выполнение запроса для извлечения user_id по нику
        query = "SELECT chat_id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        else:
            print(f"Пользователь с ником {username} не найден.")
            return None
        
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return None
    
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")

async def save_invited_user_by_invite_code(state, invited_user_id):
    data = await state.get_data()
    invite_code = data['invite_code']
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Найти user_id агента по invite_code
        query = "SELECT user_id FROM agents WHERE invite_code = %s"
        cursor.execute(query, (invite_code,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]

            # Добавить запись в таблицу invited_users
            insert_query = "INSERT INTO invited_users (user_id, invited_user_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, invited_user_id))
            conn.commit()

            await bot.send_message(user_id, f"Пользователь {invited_user_id} был приглашел агентом {user_id}.")
        else:
            await bot.send_message(invited_user_id, f"Инвайт-код {invite_code} не найден.")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Database connection closed.")

async def delete_agent_by_username(state, chat_id):
    data = await state.get_data()
    username = data['name']
    user_id = get_user_id_by_username(username)
    if not user_id:
        print(f"Пользователь с именем {username} не найден.")
        return

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Удаление агента по user_id
        cursor.execute("DELETE FROM agents WHERE user_id = %s", (user_id,))
        conn.commit()

        if cursor.rowcount > 0:
            await bot.send_message(chat_id, f"Агент с user_id {user_id} успешно удален.")
        else:
            await bot.send_message(chat_id, f"Агент с user_id {user_id} не найден в таблице agents.")

    except mysql.connector.Error as err:
        await bot.send_message(chat_id, f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрываем соединение с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def add_category(state, user_id):
    data = await state.get_data()
    name = data['name']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL-запрос для добавления новой категории
        query = "INSERT INTO categories (name) VALUES (%s)"
        cursor.execute(query, (name,))

        # Подтверждение транзакции
        conn.commit()
        await bot.send_message(user_id, "Категория добавлена успешно")

    except:
        await bot.send_message(user_id, f"Ошибка при работе с базой данных")

    finally:
        # Закрытие соединения с базой данных
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def delete_category(state, user_id):
    data = await state.get_data()
    name = data['name']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL-запрос для удаления категории по названию
        query = "DELETE FROM categories WHERE name = %s"
        cursor.execute(query, (name,))

        # Подтверждение транзакции
        conn.commit()

        if cursor.rowcount > 0:
            await bot.send_message(user_id, "Категория удалена успешно")
        else:
            await bot.send_message(user_id, "Категория с таким названием не найдена")

    except:
        await bot.send_message(user_id, f"Ошибка при работе с базой данных")

    finally:
        # Закрытие соединения с базой данных
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def add_product(state, user_id):
    data = await state.get_data()
    name = data['product_name']
    price = data['price']
    category = data['category']
    characteristics = data['characteristics']
    description = data['description']
    availability = 1
    delivery_time = data['delivery_time']
    photo_data = data['photo_data']
    image_data = photo_data.file_id

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL запрос для добавления продукта
        add_product_query = """
            INSERT INTO products (category, name, characteristics, description, price, availability, delivery_time, image_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        product_data = (category, name, characteristics, description, price, availability, delivery_time, image_data)

        # Выполнение запроса
        cursor.execute(add_product_query, product_data)
        conn.commit()

        await bot.send_message(user_id, "Продукт успешно добавлен")

    except mysql.connector.Error as err:
        await bot.send_message(user_id, f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def delete_product_by_category_and_name(state, user_id):
    data = await state.get_data()
    category = data['category']
    product_name = data['product_name']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQL запрос для удаления продукта по категории и названию
        delete_product_query = "DELETE FROM products WHERE category = %s AND name = %s"
        cursor.execute(delete_product_query, (category, product_name))

        # Подтверждение изменений
        conn.commit()

        if cursor.rowcount > 0:
            await bot.send_message(user_id, f"Продукт с категорией '{category}' и названием '{product_name}' успешно удален")
        else:
            await bot.send_message(user_id, f"Продукт с категорией '{category}' и названием '{product_name}' не найден")

    except mysql.connector.Error as err:
        await bot.send_message(user_id, f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def send_message_to_all_users(state):
    data = await state.get_data()
    message_text = data['text']
    photo_data = data['photo_data']
    image_data = photo_data.file_id
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Получение всех chat_id из таблицы users
        cursor.execute("SELECT chat_id FROM users")
        chat_ids = cursor.fetchall()

        # Отправка сообщения каждому chat_id
        for chat_id in chat_ids:
            await bot.send_photo(chat_id=chat_id[0], photo=image_data, caption=message_text)

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрываем соединение с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def export_users_balance_to_excel_and_send(chat_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)

        # Запрос для извлечения данных
        query = """
            SELECT u.id AS ID, u.username AS Username, p.balance AS Balance
            FROM users u
            LEFT JOIN profiles p ON u.id = p.user_id
        """

        # Чтение данных с помощью Pandas
        df = pd.read_sql(query, conn)

        # Генерация имени для Excel файла
        excel_filename = 'users_balance.xlsx'

        # Сохранение DataFrame в Excel
        df.to_excel(excel_filename, index=False)
        document = FSInputFile(excel_filename)

        await bot.send_document(chat_id, document)

        print(f"Отправлен Excel файл с балансами пользователю {chat_id}")

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")

# invite_link = f"https://t.me/dark_c0d3_bot?start={invite_code}"

async def send_agent_info(user_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Запрос для извлечения данных агента по user_id
        query = """
            SELECT invite_code, invited_users, earnings
            FROM agents
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            invite_code, invited_users, earnings = result

            # Формирование сообщения
            message_text = (
                f"Информация агента:\n\n"
                f"индивидуальная ссылка: https://t.me/dark_c0d3_bot?start={invite_code}\n"
                f"Количество приглашенных пользователей: {invited_users}\n"
                f"Заработанные деньги: {earnings} USDT."
            )

            # Отправка сообщения пользователю
            await bot.send_message(chat_id=user_id, text=message_text, reply_markup=kb.agent_kb)
        else:
            # Если данных для данного user_id нет
            await bot.send_message(chat_id=user_id, text="Информация о вас как об агенте не найдена.")

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def create_invite_link_group(group_id):
    invite_link = await bot.create_chat_invite_link(chat_id=group_id, expire_date=None, member_limit=1)
    return invite_link.invite_link

async def check_subscription_and_invite(user_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Запрос для проверки подписки пользователя по user_id
        query = """
            SELECT subscription_end
            FROM profiles
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            subscription_end = result[0]
            current_date = datetime.now().date()

            if subscription_end and subscription_end > current_date:
                # Если подписка активна, создаем ссылку приглашения и отправляем пользователю
                invite_link = await create_invite_link_group(-4208340770)
                await bot.send_message(chat_id=user_id, text=f"Ваша подписка активна! Присоединяйтесь к группе по ссылке: {invite_link}")
            else:
                # Если подписка неактивна, отправляем личное сообщение пользователю
                await bot.send_message(chat_id=user_id, text="Ваша подписка истекла. Пожалуйста, продлите подписку.")
        else:
            # Если данных для данного user_id нет
            await bot.send_message(chat_id=user_id, text="Информация о подписке не найдена.")

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def check_balance_send_message_and_reset(user_id: int, cash, name):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Запрос для получения баланса пользователя
        query = "SELECT earnings FROM agents WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            balance = result[0]

            # Проверка баланса и отправка соответствующего сообщения
            if balance >= 10:
                message = "У вас достаточно средств на балансе. Баланс будет обнулен."
                # Обнуление баланса
                update_query = "UPDATE agents SET earnings = 0 WHERE user_id = %s"
                cursor.execute(update_query, (user_id,))
                conn.commit()
                await bot.send_message(chat_id=-4208340770, text=f"Пользователь @{name} отправил запрос на вывод {balance}USDT на кошелёк {cash}")
            else:
                message = "У вас недостаточно средств на балансе."

            await bot.send_message(user_id, message)

        else:
            await bot.send_message(user_id, "Пользователь не найден.")

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрытие соединения с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")
