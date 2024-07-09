from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

# Клавиатура для обычного пользователя
user_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Каталог", callback_data="catalog"),
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
    ],
    [
        InlineKeyboardButton(text="Закрытый чат", callback_data="closed_chat"),
    ],
    [
        InlineKeyboardButton(text="Доставка", url="https://example.com/delivery"),
        InlineKeyboardButton(text="О Нас", url="https://telegra.ph/O-nas-06-26-2"),
        InlineKeyboardButton(text="Менеджер", url="https://example.com/guarantees"),
    ]
])

# Клавиатура для агента
agent_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Каталог", callback_data="catalog"),
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
    ],
    [
        InlineKeyboardButton(text="Закрытый чат", callback_data="closed_chat"),
    ],
    [
        InlineKeyboardButton(text="Доставка", url="https://example.com/delivery"),
        InlineKeyboardButton(text="О Нас", url="https://telegra.ph/O-nas-06-26-2"),
        InlineKeyboardButton(text="Менеджер", url="https://example.com/guarantees"),
    ],
    [
        InlineKeyboardButton(text="Агент", callback_data="agent"),
    ]
])

# Клавиатура профиля
profile_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Покупки", callback_data="purchases")
    ],
    [
        InlineKeyboardButton(text="Пополнить баланс", callback_data="top_up_balance"),
        InlineKeyboardButton(text="Продлить подписку", callback_data="extend_subscription"),
    ],
    [
        InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")
    ]
])

shop_kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить", callback_data="buy"),
        InlineKeyboardButton(text="Отзывы", callback_data="rev"),
    ],
    [
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ],
    [
        InlineKeyboardButton(text="Следующий товар >", callback_data="next_prod"),
    ]
])

shop_kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить", callback_data="buy"),
        InlineKeyboardButton(text="Отзывы", callback_data="rev"),
    ],
    [
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ],
    [
        InlineKeyboardButton(text="<", callback_data="prev_prod"),
        InlineKeyboardButton(text=">", callback_data="next_prod"),
    ]
])

shop_kb_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить", callback_data="buy"),
        InlineKeyboardButton(text="Отзывы", callback_data="rev"),
    ],
    [
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ],
    [
        InlineKeyboardButton(text="< Предыдущий товар", callback_data="prev_prod"),
    ]
])

shop_kb_4 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить", callback_data="buy"),
        InlineKeyboardButton(text="Отзывы", callback_data="rev"),
    ],
    [
        InlineKeyboardButton(text="Меню", callback_data="menu"),
    ]
])

rev_kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотреть отзывы", callback_data="rev_look"),],
        [InlineKeyboardButton(text="Оставить отзыв", callback_data="rev_write"),],
        [InlineKeyboardButton(text="Обратно к товару", callback_data='back_to_prod'),]
])

rev_kb_wr = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Положительный", callback_data="good"),
         InlineKeyboardButton(text="Отрицательный", callback_data="bad"),],
        [InlineKeyboardButton(text="Обратно к товару", callback_data='back_to_prod'),]
])

rev_kb_wr_2 = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Редактировать", callback_data="red"),],
        [InlineKeyboardButton(text="Опубликовать", callback_data="pub"),],
        [InlineKeyboardButton(text="Обратно к товару", callback_data='back_to_prod'),]
])

rev_kb_1 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обратно к товару", callback_data="back_to_prod"),
    ],
    [
        InlineKeyboardButton(text="Следующий отзыв >", callback_data="next_rev"),
    ]
])

rev_kb_2 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обратно к товару", callback_data="back_to_prod"),
    ],
    [
        InlineKeyboardButton(text="<", callback_data="prev_rev"),
        InlineKeyboardButton(text=">", callback_data="next_rev"),
    ]
])

rev_kb_3 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обратно к товару", callback_data="back_to_prod"),
    ],
    [
        InlineKeyboardButton(text="Предыдущий отзыв <", callback_data="prev_rev"),
    ]
])

rev_kb_4 = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Обратно к товару", callback_data="back_to_prod"),
    ]
])

menu_adm = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Каталог", callback_data="catalog"),
        InlineKeyboardButton(text="Профиль", callback_data="profile"),
    ],
    [
        InlineKeyboardButton(text="Закрытый чат", callback_data="closed_chat"),
    ],
    [
        InlineKeyboardButton(text="Доставка", url="https://example.com/delivery"),
        InlineKeyboardButton(text="О Нас", url="https://telegra.ph/O-nas-06-26-2"),
        InlineKeyboardButton(text="Менеджер", url="https://example.com/guarantees"),
    ],
    [
        InlineKeyboardButton(text="Админ", callback_data="adm_adm"),
    ]
])

main_admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")
    ],
    [
        InlineKeyboardButton(text="Добавить администратора", callback_data="admin_add"),
        InlineKeyboardButton(text="Добавить агента", callback_data="agent_add")
    ],
    [
        InlineKeyboardButton(text="Удалить администратора", callback_data="admin_del"),
        InlineKeyboardButton(text="Удалить агента", callback_data="agent_del")
    ],
    [
        InlineKeyboardButton(text="Добавить категорию", callback_data="category_add"),
        InlineKeyboardButton(text="Добавить товар", callback_data="prod_add"),
    ],
    [
        InlineKeyboardButton(text="Удалить категорию", callback_data="category_del"),
        InlineKeyboardButton(text="Удалить товар", callback_data="prod_del"),
    ],
    [InlineKeyboardButton(text="Создать рассылку", callback_data="send_all"),],
    [InlineKeyboardButton(text="Без картинки", callback_data="send_"),],
    [InlineKeyboardButton(text="Выгрузить остатки баланса", callback_data="exel_get"),]
])

admin_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вернуться в меню", callback_data="back_to_menu")
    ],
    [
        InlineKeyboardButton(text="Добавить агента", callback_data="agent_add")
    ],
    [
        InlineKeyboardButton(text="Удалить агента", callback_data="agent_del")
    ],
    [
        InlineKeyboardButton(text="Добавить категорию", callback_data="category_add"),
        InlineKeyboardButton(text="Добавить товар", callback_data="prod_add"),
    ],
    [
        InlineKeyboardButton(text="Удалить категорию", callback_data="category_del"),
        InlineKeyboardButton(text="Удалить товар", callback_data="prod_del"),
    ],
    [InlineKeyboardButton(text="Создать рассылку", callback_data="send_all"),],
    [InlineKeyboardButton(text="Без картинки", callback_data="send_"),],
    [InlineKeyboardButton(text="Выгрузить остатки баланса", callback_data="exel_get"),]
])

admin_add_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Главный администратор", callback_data="main_admin_add"),
    ],
    [
        InlineKeyboardButton(text="Администратор", callback_data="admin_add_"),
    ],
    [
        InlineKeyboardButton(text="Обратно в меню", callback_data="back_to_menu"),
    ]
])

agent_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Вывести", callback_data="agent_withdraw"),
    ],
    [
        InlineKeyboardButton(text="В меню", callback_data="back_to_menu"),
    ]
])

sub_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Месяц", callback_data="1")
    ],
    [
        InlineKeyboardButton(text="3 Месяца", callback_data="3"),
    ],
    [
        InlineKeyboardButton(text="12 Месяцев", callback_data="12"),
    ]
])

buy_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Заказ", callback_data="order")
    ],
    [
        InlineKeyboardButton(text="Купить сразу", callback_data="buy__"),
    ],
    [
        InlineKeyboardButton(text="Обратно к товару", callback_data="back_to_prod"),
    ]
])

kb_photo_edit = [
    [types.KeyboardButton(text="Удалить последнее фото")],
    [types.KeyboardButton(text="Готово")]
]

kb_photo_edit_1 = types.ReplyKeyboardMarkup(
    keyboard=kb_photo_edit,
    resize_keyboard=True
)