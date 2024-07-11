import mysql.connector
import time
from datetime import date, timedelta
from aiogram import Bot
import config
bot = Bot(token=config.BOT_TOKEN)
import asyncio

db_config = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'wFaEPSogZvh94bfu',
    'database': "tgbot"
}

async def update_subscriptions():
    # Получаем текущую дату
    today = date.today()

    # Открываем курсор для выполнения SQL запросов
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # SQL запрос для выбора всех профилей, у которых подписка заканчивается сегодня или ранее
    sql = "UPDATE profiles SET subscription_end = NULL WHERE subscription_end IS NOT NULL AND subscription_end <= %s"
    cursor.execute(sql, (today,))
    print('done')


     # SQL запрос для выбора user_id всех профилей, где подписка равна NULL
    select_sql = "SELECT user_id FROM profiles WHERE subscription_end IS NULL"
    cursor.execute(select_sql)

    # Получаем все строки результата
    user_ids = cursor.fetchall()

    # Выводим user_id всех профилей, где подписка равна NULL
    for user_data in user_ids:
        user_id = user_data['user_id']
        ch_id = -1002173050102
        try:
            await bot.ban_chat_member(ch_id, user_id)
            await bot.unban_chat_member(ch_id, user_id)
        except:
            print('pass')



    # Подтверждаем выполнение изменений в базе данных
    conn.commit()
    print('saved')
    # Закрываем курсор и соединение с базой данных
    cursor.close()

# Основной цикл программы для ежедневной проверки и обновления подписок
if __name__ == "__main__":
    while True:
        # Вызываем функцию обновления подписок
        asyncio.run(update_subscriptions())

        # Пауза на 24 часа (86400 секунд) перед следующей проверкой
        time.sleep(20)