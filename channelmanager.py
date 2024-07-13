import mysql.connector
import time
from datetime import date
from aiogram import Bot
import config
import asyncio

# Инициализация бота
bot = Bot(token=config.BOT_TOKEN)

# Конфигурация базы данных
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gq1ihzD1nVW20m50izf6',
    'database': 'telegram_bot'
}

async def update_subscriptions():
    try:
        # Получаем текущую дату
        today = date.today()

        # Открываем соединение с базой данных
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Обновляем подписки для профилей, у которых подписка заканчивается сегодня или ранее
        sql_update = "UPDATE profiles SET subscription_end = NULL WHERE subscription_end IS NOT NULL AND subscription_end <= %s"
        cursor.execute(sql_update, (today,))
        conn.commit()
        print('Subscription updates done.')

        # Получаем список пользователей с истекшими подписками
        sql_select = "SELECT user_id FROM profiles WHERE subscription_end IS NULL"
        cursor.execute(sql_select)
        user_ids = cursor.fetchall()

        # Выполняем действия с пользователями
        ch_id = -1002173050102  # ID чата, в котором выполняем действия

        for user_data in user_ids:
            user_id = user_data['user_id']
            try:
                await bot.ban_chat_member(ch_id, user_id)
                await bot.unban_chat_member(ch_id, user_id)
                print(f'User {user_id} banned and unbanned.')
            except Exception as e:
                print(f'Error processing user {user_id}: {e}')

    except mysql.connector.Error as err:
        print(f"MySQL error: {err}")
    finally:
        # Закрываем курсор и соединение с базой данных
        cursor.close()
        conn.close()

# Основной цикл программы для ежедневной проверки и обновления подписок
if __name__ == "__main__":
    try:
        while True:
            asyncio.run(update_subscriptions())
            # Пауза на 24 часа (86400 секунд) перед следующей проверкой
            time.sleep(86400)  # Изменил на сутки между проверками
    except KeyboardInterrupt:
        print("Script stopped by user.")
