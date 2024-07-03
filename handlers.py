from aiogram import F, Router, types
from aiogram import Bot
import aiogram.utils
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import logging

import kb
import text
import db
import utils
import config

import test

bot = Bot(token=config.BOT_TOKEN)

logging.basicConfig(level=logging.INFO)

router = Router()

class AdminState(StatesGroup):
    admin = State()
    admin_add = State()
    admin_del = State()
    admin_agent = State()
    admin_agent_del = State()
    category_add = State()
    category_del = State()
    product_add = State()
    product_add_1 = State()
    product_add_2 = State()
    product_add_3 = State()
    product_add_4 = State()
    product_add_5 = State()
    product_add_6 = State()
    product_del = State()
    product_del_1 = State()
    send_add = State()
    send_add_ = State()

class CatalogState(StatesGroup):
    catalog = State()
    catalog_prod = State()
    catalog_rev_look = State()
    catalog_rev = State()
    catalog_rev_write = State()
    catalog_rev_write_0 = State()
    catalog_rev_write_1 = State()
    catalog_rev_write_2 = State()
    catalog_rev_write_3 = State()
    agent_withdraw = State()
    agent_withdraw_1 = State()


@router.message(Command('get_group_id'))
async def group_handler(msg: Message, state: FSMContext):
    await bot.send_message(msg.chat.id, text=f"chat id = {msg.chat.id}")

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    if '?start=' in msg.text:
        invite_code = msg.text.split('?start=')[1]
        await state.update_data(invite_code=invite_code)
        await utils.save_invited_user_by_invite_code(state, msg.from_user.id)
    db.check_and_create_user(msg.from_user.username, msg.from_user.id)
    await utils.send_menu_by_role(msg.from_user.id)

@router.callback_query(lambda c: c.data in ['admin_add', 'agent_add', 'admin_del', 'agent_del', 'category_add', 'prod_add', 'category_del', 'prod_del', 'send_all', 'exel_get'])
async def process_admin_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'admin_add':
        # handle admin add
        await state.set_state(AdminState.admin)
        await callback.message.answer(text='Выберите роль нового администратора.', reply_markup=kb.admin_add_kb)
    elif callback.data == 'agent_add':
        # handle agent add
        await state.set_state(AdminState.admin_agent)
        await callback.message.answer(text='Введите ник нового агента. (он должен заранее написать команду старт)')
    elif callback.data == 'admin_del':
        # handle admin delete
        await state.set_state(AdminState.admin_del)
        await callback.message.answer(text='Введите ник администратора, которого хотите удалить.')
    elif callback.data == 'agent_del':
        # handle agent delete
        await state.set_state(AdminState.admin_agent_del)
        await callback.message.answer(text='Введите ник агента, которого хотите удалить.')
    elif callback.data == 'category_add':
        # handle category add
        await state.set_state(AdminState.category_add)
        await callback.message.answer(text='Введите название новой категории категории.')
    elif callback.data == 'prod_add':
        # handle product add
        await state.set_state(AdminState.product_add)
        await utils.send_category_message(callback.from_user.id)
    elif callback.data == 'category_del':
        # handle category delete
        await state.set_state(AdminState.category_del)
        await callback.message.answer(text='Введите название категории, которую хотите удалить.')
    elif callback.data == 'prod_del':
        # handle product delete
        await state.set_state(AdminState.product_del)
        await utils.send_category_message(callback.from_user.id)
    elif callback.data == 'send_all':
        await state.set_state(AdminState.send_add_)
        await callback.message.answer('Введите сообщение для рассылки.')
    elif callback.data == 'exel_get':
        await utils.export_users_balance_to_excel_and_send(callback.from_user.id)

@router.message(AdminState.send_add_, F.text)
async def semd_add_(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await state.set_state(AdminState.send_add)
    await msg.answer('Отправьте картинку для Рассылки.')

@router.message(AdminState.send_add, F.photo)
async def send_add(msg: Message, state: FSMContext):
    await state.update_data(photo_data = msg.photo[-1])
    await utils.send_message_to_all_users(state)
    await state.clear()
    await msg.answer('Рассылка завершена.')
    await utils.send_menu_by_role(msg.from_user.id)
    

    # category VARCHAR(100) NOT NULL,
    # name VARCHAR(100) NOT NULL,
    # characteristics TEXT,
    # description TEXT,
    # price DECIMAL(10,2) NOT NULL,
    # availability TINYINT(1) DEFAULT 1,
    # delivery_time VARCHAR(100),
    # image_data TEXT

@router.callback_query(StateFilter(AdminState.admin), lambda c: c.data in ['admin_add_', 'main_admin_add, back_to_menu'])
async def admin_add(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'admin_add_':
        await state.set_state(AdminState.admin_add)
        await state.update_data(role='admin')
        await bot.send_message(callback.from_user.id, text='Введите ник пользователя. (он должен заранее написать команду старт боту)')
    elif callback.data == 'main_admin_add':
        await state.set_state(AdminState.admin_add)
        await state.update_data(role='main')
        await bot.send_message(callback.from_user.id, text='Введите ник пользователя. (он должен заранее написать команду старт боту)')
    elif callback.data == 'back_to_menu':
        await state.clear()
        await utils.send_menu_by_role(callback.from_user.id)

@router.message(AdminState.product_del, F.text)
async def product_del(msg: Message, state: FSMContext):
    if msg.text == 'обратно в меню':
        await state.clear()
        await utils.send_menu_by_role(msg.from_user.id)
    else:
        await state.update_data(category=msg.text)
        await bot.send_message(msg.from_user.id, 'Введите название продукта, который хотите удалить.')
        await state.set_state(AdminState.product_del_1)

@router.message(AdminState.product_del, F.text)
async def product_del(msg: Message, state: FSMContext):
    await state.update_data(product_name = msg.text)
    await utils.delete_product_by_category_and_name(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.product_add, F.text)
async def product_add(msg: Message, state: FSMContext):
    if msg.text == 'обратно в меню':
        await state.clear()
        await utils.send_menu_by_role(msg.from_user.id)
    else:
        await state.update_data(category=msg.text)
        await bot.send_message(msg.from_user.id, 'Введите название для нового продукта.')
        await state.set_state(AdminState.product_add_1)

@router.message(AdminState.product_add_1, F.text)
async def product_add_1(msg: Message, state: FSMContext):
    await state.update_data(product_name = msg.text)
    await bot.send_message(msg.from_user.id, 'Введите характеристики для нового продукта.')
    await state.set_state(AdminState.product_add_2)

@router.message(AdminState.product_add_2, F.text)
async def product_add_2(msg: Message, state: FSMContext):
    await state.update_data(characteristics = msg.text)
    await bot.send_message(msg.from_user.id, 'Введите описание для нового продукта.')
    await state.set_state(AdminState.product_add_3)

@router.message(AdminState.product_add_3, F.text)
async def product_add_3(msg: Message, state: FSMContext):
    await state.update_data(description = msg.text)
    await bot.send_message(msg.from_user.id, 'Введите цену для нового продукта.')
    await state.set_state(AdminState.product_add_4)

@router.message(AdminState.product_add_4, F.text)
async def product_add_4(msg: Message, state: FSMContext):
    await state.update_data(price = msg.text)
    await bot.send_message(msg.from_user.id, 'Отправьте срок доставки товара.')
    await state.set_state(AdminState.product_add_5)

@router.message(AdminState.product_add_5, F.text)
async def product_add_4(msg: Message, state: FSMContext):
    await state.update_data(delivery_time = msg.text)
    await bot.send_message(msg.from_user.id, 'Отправьте изображение товара.')
    await state.set_state(AdminState.product_add_6)

@router.message(AdminState.product_add_6, F.photo)
async def product_handler_photo(msg: Message, state: FSMContext):
    await state.update_data(photo_data = msg.photo[-1])
    # await msg.answer(f'{photo_data.file_id}')
    await utils.add_product(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.admin_add, F.text)
async def admin_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.add_admin(msg.from_user.id, state)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.admin_del, F.text)
async def admin_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_admin(msg.from_user.id, state)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.admin_agent, F.text)
async def admin_agent(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.create_invite_link(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.admin_agent_del, F.text)
async def agent_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_agent_by_username(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.category_add, F.text)
async def admin_category_add(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.add_category(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(AdminState.category_del, F.text)
async def admin_category_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_category(state, msg.from_user.id)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.callback_query(lambda c: c.data in ['catalog', 'profile', 'closed_chat', 'agent', ])
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        if callback.data == 'catalog':
            await utils.send_category_message(callback.from_user.id)
            await state.set_state(CatalogState.catalog)
        elif callback.data == 'profile':
            await utils.send_user_profile(callback.from_user.id)
        elif callback.data == 'closed_chat':
            await utils.check_subscription_and_invite(callback.from_user.id)
        elif callback.data == 'agent':
            await utils.send_agent_info(callback.from_user.id)
    except aiogram.exceptions.TelegramAPIError as e:
        # Логируем ошибку или обрабатываем ее по необходимости
        print(f"Ошибка Telegram API: {e}")

@router.callback_query(lambda c: c.data in ['purchases', 'top_up_balance', 'extend_subscription', 'back_to_menu', 'agent_withdraw'])
async def process_profile_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        if callback.data == 'purchases':
            await bot.send_message(callback.from_user.id, "Вы выбрали Покупки")
        elif callback.data == 'top_up_balance':
            await bot.send_message(callback.from_user.id, "Вы выбрали Пополнить баланс")
        elif callback.data == 'extend_subscription':
            await bot.send_message(callback.from_user.id, "Вы выбрали Продлить подписку")
        elif callback.data == 'back_to_menu':
            await utils.send_menu_by_role(callback.from_user.id)
        elif callback.data == 'agent_withdraw':
            await bot.send_message(callback.from_user.id, 'Введите номер кошелька.')
            await state.set_state(CatalogState.agent_withdraw)

    except aiogram.exceptions.TelegramAPIError as e:
        # Handle Telegram API errors
        print(f"Ошибка Telegram API: {e}")

@router.message(CatalogState.agent_withdraw, F.text)
async def agent_withdraw(msg: Message, state: FSMContext):
    await utils.check_balance_send_message_and_reset(msg.from_user.id, msg.text, msg.from_user.username)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(CatalogState.catalog, F.text)
async def catalog_handler(msg: Message, state: FSMContext):
    if msg.text == 'обратно в меню':
        await state.clear()
        await utils.send_menu_by_role(msg.from_user.id)
    else:
        await state.set_state(CatalogState.catalog_prod)
        await state.update_data(num = 0)
        await state.update_data(category = msg.text)
        await utils.send_first_product_with_image(msg.from_user.id, await state.get_data(), state)

@router.callback_query(StateFilter(CatalogState.catalog_prod),lambda c: c.data in ['buy', 'rev', 'menu', 'prev_prod', 'next_prod'])
async def catalog_prod(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'menu':
        await state.clear()
        await utils.send_menu_by_role(callback.from_user.id)
    elif callback.data in ['prev_prod', 'next_prod']:
        await utils.update_data_num(callback.data, state)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data == 'rev':
        await state.set_state(CatalogState.catalog_rev_write_0)
        await bot.send_message(chat_id=callback.from_user.id, text='Выберите опцию', reply_markup=kb.rev_kb)
    elif callback.data == 'buy':
        pass

@router.callback_query(StateFilter(CatalogState.catalog_rev_write_0),lambda c: c.data in ['rev_write', 'rev_look', 'back_to_prod'])
async def catalog_rev_write_0(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_prod':
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data == 'rev_write':
        await state.set_state(CatalogState.catalog_rev_write_1)
        await bot.send_message(chat_id=callback.from_user.id, text='Выберите тип отзыва', reply_markup=kb.rev_kb_wr)
    elif callback.data == 'rev_look':
        await state.set_state(CatalogState.catalog_rev)
        await state.update_data(rev_num = 0)
        await utils.send_first_review(callback.from_user.id, state)

@router.callback_query(StateFilter(CatalogState.catalog_rev),lambda c: c.data in ['next_rev', 'prev_rev', 'back_to_prod'])
async def catalog_rev_(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_prod':
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data in ['next_rev', 'prev_rev']:
        await utils.update_data_num(callback.data, state)
        await utils.send_first_review(callback.from_user.id, state)

@router.callback_query(StateFilter(CatalogState.catalog_rev_write_1),lambda c: c.data in ['good', 'bad', 'back_to_prod'])
async def catalog_rev_write(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_prod':
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data == 'good':
        await state.update_data(positive = True)
        await state.update_data(username = callback.from_user.username)
        await state.update_data(user_id = callback.from_user.id)
        await state.set_state(CatalogState.catalog_rev_write_2)
        await bot.send_message(chat_id=callback.from_user.id, text='Пожалуйста, напишите ваш отзыв.')
    elif callback.data == 'bad':
        await state.update_data(positive = False)
        await state.update_data(username = callback.from_user.username)
        await state.update_data(user_id = callback.from_user.id)
        await state.set_state(CatalogState.catalog_rev_write_2)
        await bot.send_message(chat_id=callback.from_user.id, text='Пожалуйста, напишите ваш отзыв.')

@router.message(CatalogState.catalog_rev_write_2, F.text)
async def catalog_rev_write_2(msg: Message, state: FSMContext):
    await state.update_data(review = msg.text)
    await state.set_state(CatalogState.catalog_rev_write_3)
    await utils.review_opt(msg.from_user.id, state)

@router.callback_query(StateFilter(CatalogState.catalog_rev_write_3),lambda c: c.data in ['red', 'pub', 'back_to_prod'])
async def catalog_rev_write_3(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_prod':
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data == 'red':
        await state.set_state(CatalogState.catalog_rev_write_2)
        await bot.send_message(chat_id=callback.from_user.id, text='Пожалуйста, напишите ваш отзыв.')
    elif callback.data == 'pub':
        await utils.add_review(state)
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)

# @router.message(CatalogState.catalog, F.photo)
# async def catalog_handler_photo(msg: Message, state: FSMContext):
#     photo_data = msg.photo[-1]
#     await msg.answer(f'{photo_data.file_id}')