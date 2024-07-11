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
from datetime import datetime, timedelta
import kb
import text
import db
import config
import aiogram.utils.media_group
import aiogram.types
from aiogram.types.input_media_photo import InputMediaPhoto
from aiogram.utils.media_group import MediaGroupBuilder
import aiomysql


bot = Bot(token=config.BOT_TOKEN)

async def send_menu_by_role(user_id: int):
    role = db.get_user_role(user_id)
    if role == 1:
        await send_user_menu(user_id)
    elif role == 2:
        await send_agent_menu(user_id)
    elif role == 3:
        await adm_adm_menu(user_id)
    elif role == 4:
        await adm_adm_menu(user_id)
    else:
        print(f"Unknown role for user {user_id}")

async def adm_adm_adm(user_id):
    role = db.get_user_role(user_id)
    if role == 3:
        await send_admin_menu(user_id)
    elif role == 4:
        await send_main_menu(user_id)

async def send_main_menu(user_id):
    await bot.send_message(user_id, 'Панель главного администратора', reply_markup=kb.main_admin_kb)

async def send_user_menu(user_id: int):
    # Отправка меню для обычного пользователя
    photo = 'AgACAgIAAxkBAAIPLWaI_X7yIyD6QfnEt0CNdB_pmWq2AAJU2jEbRa1ISBhJEqouoZ-WAQADAgADeAADNQQ'
    text = f"Отрыв Фляги— это ваш проводник в мир элегантности и стиля.\nУ нас вы найдете всё, чтобы выглядеть на все сто. Присоединяйтесь к числу наших  клиентов и наслаждайтесь роскошью по доступной цене!"
    await bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=kb.user_keyboard)

async def adm_adm_menu(user_id):
    photo = 'AgACAgIAAxkBAAIPLWaI_X7yIyD6QfnEt0CNdB_pmWq2AAJU2jEbRa1ISBhJEqouoZ-WAQADAgADeAADNQQ'
    text = f"Отрыв Фляги— это ваш проводник в мир элегантности и стиля.\nУ нас вы найдете всё, чтобы выглядеть на все сто. Присоединяйтесь к числу наших  клиентов и наслаждайтесь роскошью по доступной цене!"
    await bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=kb.menu_adm)

async def send_agent_menu(user_id: int):
    # Отправка меню для агента
    photo = 'AgACAgIAAxkBAAIPLWaI_X7yIyD6QfnEt0CNdB_pmWq2AAJU2jEbRa1ISBhJEqouoZ-WAQADAgADeAADNQQ'
    text = f"Отрыв Фляги— это ваш проводник в мир элегантности и стиля.\nУ нас вы найдете всё, чтобы выглядеть на все сто. Присоединяйтесь к числу наших  клиентов и наслаждайтесь роскошью по доступной цене!"
    await bot.send_photo(chat_id=user_id, photo=photo, caption=text, reply_markup=kb.agent_keyboard)

async def send_admin_menu(user_id: int):
    # Отправка меню для админа (если необходимо)
    await bot.send_message(user_id, "Админ панель", kb.admin_kb)

db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'wFaEPSogZvh94bfu',
    'database': "tgbot"
}

async def send_user_profile(user_id, name):
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
                subscription_status = f"Подписка действительна до: {profile_data['subscription_end'].strftime('%d.%m.%Y')}"
            else:
                subscription_status = "У вас нет активной подписки"

            message_text = f"{name}, добро пожаловать в личный кабинет. Вы можете пополнить баланс, просмотреть список покупок, а также продлить или купить подписку!\n\n"
            message_text += subscription_status + "\n"
            message_text += f"Остаток на балансе: {profile_data['balance']}"

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
    [KeyboardButton(text="Обратно в меню")],  # First row with a single button
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

async def send_first_product_with_image(chat_id: int, data, state: FSMContext):
    category_name = data['category']
    num = data['num']
    products = db.get_products_by_category(category_name)  # Предполагается, что эта функция существует и возвращает список продуктов
    
    if len(products) == 0:
        await bot.send_message(chat_id=chat_id, text='Категория пуста.')
        await state.clear()
        await send_menu_by_role(chat_id)  # Предполагается, что эта функция существует и отправляет меню в зависимости от роли
    else:
        product = products[num]
        await state.update_data(prod_id=product[0])
        image_files = product[11].split(",")  # Извлечение списка фото

        if num == 0:
            if len(products) == 1:
                keyboard = kb.shop_kb_4  # Предполагается, что это клавиатура для одного продукта
            else:
                keyboard = kb.shop_kb_1  # Предполагается, что это клавиатура для первого продукта
        elif num + 1 == len(products):
            if len(products) == 1:
                keyboard = kb.shop_kb_4
            else:
                keyboard = kb.shop_kb_3  # Предполагается, что это клавиатура для последнего продукта
        else:
            keyboard = kb.shop_kb_2  # Предполагается, что это клавиатура для промежуточных продуктов

        if product[8] == 1:
            prod_8 = 'в наличии'
        else:
            prod_8 = 'нет в наличии'

        # Создание медиа-группы
        media_group = [InputMediaPhoto(media=image_files[0], caption=f"*{product[2]}*\n\n"
                                                f"*{product[5]} Руб*\n"
                                                f"*{product[6]} USDT*\n"
                                                f"*{product[7]} USDT На официальном сайте*\n\n"
                                                f"{product[3]}\n\n"
                                                f"{product[4]}\n\n"
                                                f"*{prod_8}\n\n*"
                                                f"Обычная доставка: {product[9]}\n"
                                                f"Экспресс доставка по Москве: {product[10]}\n\n"
                                                f"{num + 1} из {len(products)}", parse_mode='Markdown')]
        for image_file in image_files[1:]:
            media_group.append(InputMediaPhoto(media=image_file))

        # Отправляем сообщение с фото и информацией о товаре
        await bot.send_media_group(chat_id, media=media_group)
        await bot.send_message(chat_id=chat_id, text='Выберите дальнейшее действие в меню:', reply_markup=keyboard)
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
        INSERT INTO reviews (username, user_id, review_text, positive, product_id, confirmed)
        VALUES (%s, %s, %s, %s, %s, FALSE)
        """
        values = (username, user_id, review_text, positive, product_id)
        
        # Выполнение запроса
        cursor.execute(query, values)
        conn.commit()
        print("Отзыв добавлен успешно.")
        
        # Получаем ID последней вставленной записи
        review_id = cursor.lastrowid
        
        # Отправка сообщения пользователю
        await bot.send_message(chat_id=user_id, text='Отзыв добавлен успешно.')

        review_info = (f"Пользователь: @{username}\n"
                           f"ID пользователя: {user_id}\n"
                           f"Отзыв: {review_text}\n"
                           f"Положительный: {'Да' if positive else 'Нет'}\n"
                           f"ID продукта: {product_id}\n"
                           f"ID отзыва в базе данных: {review_id}")

        # Отправка сообщения в группу
        await bot.send_message(chat_id=-1002166667106, text=review_info)
        
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

        # Запрос для получения всех подтвержденных отзывов по product_id
        query = "SELECT * FROM reviews WHERE product_id = %s AND confirmed = TRUE"
        cursor.execute(query, (product_id,))
        reviews = cursor.fetchall()

        if rev_num == 0:
            if len(reviews) == 1:
                keyboard = kb.rev_kb_4
            else:
                keyboard = kb.rev_kb_1
        elif rev_num + 1 == len(reviews):
            if len(reviews) == 1:
                keyboard = kb.rev_kb_4
            else:
                keyboard = kb.rev_kb_3
        else:
            keyboard = kb.rev_kb_2
        
        # Если есть подтвержденные отзывы, отправляем первый
        if reviews:
            first_review = reviews[rev_num]
            review_text = (f"{'Положительный' if first_review[4] else 'Отрицательный'} отзыв от пользователя {first_review[1]}\n\n"
                           f"{first_review[3]}\n\n"
                           f"{rev_num+1} из {len(reviews)}")
            await bot.send_message(chat_id=chat_id, text=review_text, reply_markup=keyboard)
            return True
        else:
            await bot.send_message(chat_id=chat_id, text="Отзывов для данного продукта нет.")
            await send_first_product_with_image(chat_id, data, state)
            return False

    
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
    invite_code = user_id
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
            await update_invited_users_count(user_id)

            # Добавить запись в таблицу invited_users
            insert_query = "INSERT INTO invited_users (user_id, invited_user_id) VALUES (%s, %s)"
            cursor.execute(insert_query, (user_id, invited_user_id))
            conn.commit()

            await bot.send_message(user_id, f"Пользователь {invited_user_id} был приглашен агентом {user_id}.")
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

async def update_invited_users_count(user_id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Увеличить количество приглашенных пользователей на 1
        update_query = "UPDATE agents SET invited_users = invited_users + 1 WHERE user_id = %s"
        cursor.execute(update_query, (user_id,))
        conn.commit()

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
    price_usdt = data['price_usdt']
    price_official = data['price_official']
    category = data['category']
    characteristics = data['characteristics']
    description = data['description']
    availability = 1
    normal_delivery_time = data['normal_delivery_time']
    express_delivery_time = data['express_delivery_time']
    photo_data = data['photo_data']
    if photo_data:

        image_data = ",".join(photo_data)  # Сохранение всех фото как строки, разделенной запятыми

        try:
            # Подключение к базе данных
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # SQL запрос для добавления продукта
            add_product_query = """
                INSERT INTO products (category, name, characteristics, description, price, price_usdt, price_official, availability, regular_delivery_time, express_delivery_time, image_data)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            product_data = (category, name, characteristics, description, price, price_usdt, price_official, availability, normal_delivery_time, express_delivery_time, image_data)

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
            await state.clear()
            await adm_adm_adm(user_id)
    else:
        await bot.send_message(user_id, 'Вы не добавили фотографий.')


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

async def send_message_to_all_users_(state, sender_id):
    data = await state.get_data()
    message_text = data['text']
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Получение всех chat_id из таблицы users
        cursor.execute("SELECT chat_id FROM users")
        chat_ids = cursor.fetchall()

        # Отправка сообщения каждому chat_id
        for chat_id in chat_ids:
            await bot.send_message(chat_id=chat_id[0], text=message_text)
            print('sent to', chat_id[0])
        await bot.send_message(sender_id, 'Рассылка завершена.')
        await adm_adm_adm(sender_id)

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")

    finally:
        # Закрываем соединение с базой данных
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")

async def send_message_to_all_users(state, sender_id):
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
            print('sent to', chat_id[0])
        await bot.send_message(sender_id, 'Рассылка завершена.')
        await adm_adm_adm(sender_id)

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
        print("Подключение к базе данных установлено.")

        # Запрос для извлечения данных из users
        users_query = "SELECT chat_id AS ChatID, username AS Username FROM users"
        users_df = pd.read_sql(users_query, conn)
        print("Данные пользователей успешно извлечены из базы данных.")

        # Запрос для извлечения данных из profiles
        profiles_query = "SELECT user_id AS ChatID, balance AS Balance FROM profiles WHERE balance != 0"
        profiles_df = pd.read_sql(profiles_query, conn)
        print("Данные профилей успешно извлечены из базы данных.")

        # Объединение данных
        merged_df = pd.merge(users_df, profiles_df, on='ChatID')
        merged_df = merged_df[['ChatID', 'Username', 'Balance']]  # Упорядочим колонки

        # Преобразование ChatID в строковый формат
        merged_df['ChatID'] = merged_df['ChatID'].astype(str)
        print("Данные успешно объединены и преобразованы.")

        # Генерация имени для Excel файла
        excel_filename = 'users_balance.xlsx'

        # Сохранение DataFrame в Excel
        merged_df.to_excel(excel_filename, index=False)
        print(f"Файл {excel_filename} успешно создан.")

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

async def check_subscription_and_invite(user_id, username):
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
                invite_link = await create_invite_link_group(-1002173050102)
                await bot.send_message(chat_id=user_id, text=f"Ваша подписка активна! Присоединяйтесь к группе по ссылке: {invite_link}")
            else:
                # Если подписка неактивна, отправляем личное сообщение пользователю
                await bot.send_message(chat_id=user_id, text="Ваша подписка истекла. Пожалуйста, продлите подписку в профиле.")
                await send_user_profile(user_id, username)

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
                await bot.send_message(chat_id=-1002238486562, text=f"Пользователь @{name} отправил запрос на вывод {balance}USDT на кошелёк {cash}\nid агента - {user_id}")
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

async def check_and_update_subscription(user_id, username, tarif):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve user's balance and subscription end date
        cursor.execute("SELECT balance, subscription_end FROM profiles WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            balance = user_data[0]
            subscription_end = user_data[1]
            if balance >= 30:
                # Calculate new subscription end date (extend by 30 days)
                if tarif == '1':

                    # Calculate new subscription end date (extend by 30 days)
                    if subscription_end:
                        new_subscription_end = subscription_end + timedelta(days=30)
                    else:
                        new_subscription_end = datetime.now() + timedelta(days=30)

                    # Update subscription_end and balance in the database
                    cursor.execute("UPDATE profiles SET subscription_end = %s, balance = balance - 30 WHERE user_id = %s",
                                (new_subscription_end, user_id))
                    conn.commit()
                elif tarif == '3':
                     # Calculate new subscription end date (extend by 30 days)
                    if subscription_end:
                        new_subscription_end = subscription_end + timedelta(days=90)
                    else:
                        new_subscription_end = datetime.now() + timedelta(days=90)

                    # Update subscription_end and balance in the database
                    cursor.execute("UPDATE profiles SET subscription_end = %s, balance = balance - 90 WHERE user_id = %s",
                                (new_subscription_end, user_id))
                    conn.commit()
                elif tarif == '12':
                    # Calculate new subscription end date (extend by 30 days)
                    if subscription_end:
                        new_subscription_end = subscription_end + timedelta(days=365)
                    else:
                        new_subscription_end = datetime.now() + timedelta(days=365)

                    # Update subscription_end and balance in the database
                    cursor.execute("UPDATE profiles SET subscription_end = %s, balance = balance - 150 WHERE user_id = %s",
                                (new_subscription_end, user_id))
                    conn.commit()

                await bot.send_message(chat_id=user_id, text=f"Подписка продлена до {new_subscription_end}")
                await send_user_profile(user_id, username)
            else:
                await bot.send_message(chat_id=user_id, text=f"Недостаточно баланса для продления подписки. Вы можете пополнить свой баланс в профиле.")
                await send_user_profile(user_id, username)

        else:
            print(f"User with user_id {user_id} not found in profiles table.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if 'conn' in locals():
            cursor.close()
            conn.close()

async def purchase_item(user_id, state, name):
    data = await state.get_data()
    order_info = data['order_info']
    product_id = data['num']
    category_name = data['category']
    purchase_type = data['purchase_type']

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Получение баланса и имени пользователя
        cursor.execute("SELECT balance, user_id FROM profiles WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data:
            balance = user_data[0]

            # Получение цены товара в USDT из категории
            products = db.get_products_by_category(category_name)
            if products:
                product = products[product_id]
                if product:
                    price_usdt = product[6]  # Предполагаем, что цена в USDT находится в 7-м столбце (индекс 6)
                    product_name = product[2]  # Предполагаем, что название продукта находится в 3-м столбце (индекс 2)

                    if balance >= price_usdt:
                        # Вычитание стоимости из баланса пользователя и обновление в базе данных
                        new_balance = balance - price_usdt
                        cursor.execute("UPDATE profiles SET balance = %s WHERE user_id = %s", (new_balance, user_id))
                        conn.commit()

                        # Вставка информации о покупке в таблицу заказов
                        order_date = datetime.now().strftime('%Y-%m-%d')

                        cursor.execute(
                            "INSERT INTO orders (user_id, username, order_date, order_type, product_name, order_info, price, product_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (user_id, name, order_date, purchase_type, product_name, order_info, price_usdt, product[0])
                        )
                        conn.commit()

                        await bot.send_message(user_id, f"Покупка успешно совершена. Ваш баланс составляет {new_balance} USDT.\nНе забудьте оставить отзыв!")
                        adm_txt = (f"Пользователь @{name} сделал заказ.\n\n"
                                   f"Стоимость заказа составляет: {price_usdt} USDT\n"
                                   f"Название товара: {product_name}\n"
                                   f"Тип заказа: {purchase_type}\n"
                                   f"Дата заказа: {order_date}\n"
                                   f"Информация о заказе: {order_info}\n"
                                   f"ID товара: {product[0]}")
                        await bot.send_message(-1002238486562, adm_txt)

                        cursor.execute("SELECT user_id FROM invited_users WHERE invited_user_id = %s", (user_id,))
                        result_1 = cursor.fetchone()
                        if result_1:
                            print('result = ', result_1)
                            agent_user_id = result_1[0]
                            cursor.execute("SELECT earnings FROM agents WHERE user_id = %s", (agent_user_id,))
                            current_earnings = cursor.fetchone()
                            current_earnings = current_earnings[0]
                            percent = 0.05
                            price_usdt_float = float(price_usdt)
                            earnings_to_add = price_usdt_float * percent

                            # Обновляем earnings агента
                            new_earnings = float(current_earnings) + earnings_to_add
                            update_query = "UPDATE agents SET earnings = %s WHERE user_id = %s"
                            cursor.execute(update_query, (new_earnings, agent_user_id))
                            conn.commit()

                    else:
                        await bot.send_message(user_id, "Денег на балансе недостаточно для совершения покупки, пополните баланс в профиле.")
                else:
                    await bot.send_message(user_id, f"Продукт с ID {product[0]} не найден в категории {category_name}.")
            else:
                await bot.send_message(user_id, f"Нет продуктов в категории {category_name}.")
        else:
            await bot.send_message(user_id, f"Пользователь с user_id {user_id} не найден в таблице профилей.")
    except mysql.connector.Error as err:
        await bot.send_message(user_id, f"Ошибка базы данных: {err}")
    finally:
        cursor.fetchall()
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

async def get_user_orders(user_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve user's orders
        cursor.execute("SELECT product_name, order_date, order_type, price FROM orders WHERE user_id = %s", (user_id,))
        orders = cursor.fetchall()

        if orders:
            order_list = []
            for order in orders:
                product_name, order_date, order_type, price = order
                order_date = order_date.strftime('%Y-%m-%d')
                order_list.append(f"Название товара: {product_name}\nДата: {order_date}\nТип заказа: {order_type}\nЦена: {price} USDT")

            order_message = "\n\n".join(order_list)
            await bot.send_message(user_id, f"Ваши заказы:\n\n{order_message}")
        else:
            await bot.send_message(user_id, "У вас нет заказов.")

    except mysql.connector.Error as err:
        await bot.send_message(user_id, f"Ошибка базы данных: {err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

async def check_order_existence(user_id, state):
    data = await state.get_data()
    category_name = data['category']
    product_id = data['num']

    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Получение имени продукта на основе product_id и category_name
        products = db.get_products_by_category(category_name)
        product = products[product_id]
        tovar_id = product[0]
        print(tovar_id)

        if product:
            # Проверка существования заказа для пользователя с этим именем продукта и идентификатором продукта
            cursor.execute("SELECT * FROM orders WHERE user_id = %s AND product_id = %s", (user_id, tovar_id))
            existing_order = cursor.fetchone()
            print(existing_order)

            if existing_order:
                return True  # Заказ уже существует
            else:
                return False  # Заказ не существует

        else:
            return False  # Продукт не найден

    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return False

    finally:
        cursor.fetchall()
        try:
            if cursor:
                cursor.close()
        except mysql.connector.Error as err:
            print(f"Ошибка при закрытии курсора: {err}")
        try:
            if conn and conn.is_connected():
                conn.close()
        except mysql.connector.Error as err:
            print(f"Ошибка при закрытии соединения: {err}")
    
async def confirm_review(review_id: int) -> bool:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("UPDATE reviews SET confirmed = 1 WHERE id = %s", (review_id,))
        conn.commit()
        return cursor.rowcount > 0  # Возвращает True, если была изменена хотя бы одна строка
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

async def delete_review(review_id: int) -> bool:
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
        conn.commit()
        return cursor.rowcount > 0  # Возвращает True, если была удалена хотя бы одна строка
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
        return False
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

async def photo_add_to_list(p_data, state, user_id):
    data = await state.get_data()
    photo_from_data_list = data['photo_data']
    p_data_id = p_data.file_id

    photo_from_data_list.append(p_data_id)
    await state.update_data(photo_data=photo_from_data_list)

    # Create media group list
    media_group = []
    for idx, photo in enumerate(photo_from_data_list):
        if idx == 0:
            media_group.append(InputMediaPhoto(media=photo, caption="Картинки товара."))
        else:
            media_group.append(InputMediaPhoto(media=photo))

    if media_group:
        await bot.send_media_group(chat_id=user_id, media=media_group)

async def remove_last_photo_and_send(user_id, state):
    data = await state.get_data()
    photo_from_data_list = data['photo_data']

    if photo_from_data_list:
        # Удаляем последнее фото из списка
        removed_photo_id = photo_from_data_list.pop()

        # Обновляем данные в состоянии
        await state.update_data(photo_data=photo_from_data_list)

        # Создаем медиа-группу
        media_group = []
        for idx, photo in enumerate(photo_from_data_list):
            if idx == 0:
                media_group.append(InputMediaPhoto(media=photo, caption="Картинки товара."))
            else:
                media_group.append(InputMediaPhoto(media=photo))
        
        if media_group:
            # Отправляем медиа-группу
            await bot.send_media_group(chat_id=user_id, media=media_group)
        else:
            await bot.send_message(user_id, 'Фотография удалена.')
    
    else:
        # Отправляем сообщение о том, что не добавлено фотографий
        await bot.send_message(chat_id=user_id, text="Вы не добавили фотографий.")

async def check_subscriptions():
    try:
        # Подключение к MySQL
        conn = await aiomysql.connect(**db_config)
        cursor = await conn.cursor()

        # Находим всех пользователей, у которых подписка заканчивается сегодня
        today = datetime.date.today()
        sql = "SELECT user_id FROM profiles WHERE subscription_end = %s"
        await cursor.execute(sql, (today,))
        profiles_to_update = await cursor.fetchall()

        # Обновляем subscription_end на NULL и удаляем из канала
        for (user_id,) in profiles_to_update:
            await cursor.execute("UPDATE profiles SET subscription_end = NULL WHERE user_id = %s", (user_id,))
            await bot.kick_chat_member(chat_id=-1002173050102, user_id=user_id)

        await conn.commit()
        print("Daily subscription check completed.")

        await cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error during daily subscription check: {e}")

