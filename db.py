import mysql.connector
import config
from datetime import datetime
from mysql.connector import Error
import mimetypes

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gq1ihzD1nVW20m50izf6',
    'database': "telegram_bot"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def check_and_create_user(username, chat_id):
    try:
        # Connect to the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if the user exists by chat_id
        cursor.execute("SELECT id FROM users WHERE chat_id = %s", (chat_id,))
        user_exists = cursor.fetchone()

        if user_exists:
            print("User already exists.")
            return False
        else:
            # Insert a new user into users table
            cursor.execute("INSERT INTO users (username, chat_id, created_at) VALUES (%s, %s, %s)",
                           (username, chat_id, datetime.now()))
            
            # Insert a default profile for the new user with the same user_id
            cursor.execute("INSERT INTO profiles (user_id, balance, subscription_end, agent) VALUES (%s, 0.00, NULL, FALSE)",
                           (chat_id,))
            
            conn.commit()
            print("User successfully registered.")
            return True

    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Database error: {err}")
        return False

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

def get_user_role(user_id):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Проверка роли пользователя по таблице admin
        cursor.execute("SELECT role FROM admin WHERE user_id = %s", (user_id,))
        admin_role = cursor.fetchone()
        if admin_role:
            if admin_role[0] == 'main':
                return 4  # Пользователь является главным администратором
            else:
                return 3  # Пользователь является администратором

        # Проверка роли пользователя по таблице agents
        cursor.execute("SELECT id FROM agents WHERE user_id = %s", (user_id,))
        agent_exists = cursor.fetchone()
        if agent_exists:
            return 2  # Пользователь является агентом

        # Если пользователь не агент и не администратор, считаем его обычным пользователем
        return 1

    except mysql.connector.Error as err:
        print(f"Ошибка при работе с базой данных: {err}")
        return None

    finally:
        # Закрываем соединение с базой данных
        cursor.fetchall()
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Соединение с базой данных закрыто.")


def get_products_by_category(category_name):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM products WHERE category = %s", (category_name,))
        products = cursor.fetchall()
        print(products)
        return products

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("Database connection closed.")

def add_product(category, name, characteristics, description, price, availability, delivery_time, image_path):
    try:
        # Подключение к базе данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        # Определение mime-типа изображения
        mime_type, _ = mimetypes.guess_type(image_path)
        if mime_type not in ['image/jpeg', 'image/png', 'image/gif']:
            raise ValueError("Неподдерживаемый формат изображения. Поддерживаются только JPEG, PNG и GIF.")
        
        # SQL-запрос для вставки данных
        query = """
        INSERT INTO products (category, name, characteristics, description, price, availability, delivery_time, image_data)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Вставка данных, включая путь к изображению
        values = (category, name, characteristics, description, price, availability, delivery_time, image_path)
        
        # Выполнение запроса
        cursor.execute(query, values)
        conn.commit()
        print("Продукт добавлен успешно.")
        
    except mysql.connector.Error as err:
        print(f"Ошибка базы данных: {err}")
    
    except ValueError as ve:
        print(f"Ошибка при обработке изображения: {ve}")
    
    except Exception as ex:
        print(f"Произошла ошибка: {ex}")
    
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None and conn.is_connected():
            conn.close()
            print("Соединение с базой данных закрыто.")

# Пример использования функции с новой структурой
#add_product('Electronics', 'Smartphone', 'Various characteristics', 'Description here', 299.99, 1, '3-5 days', r'C:\Users\US\zakaz_shop\images.jpg')
