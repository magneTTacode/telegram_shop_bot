from aiogram import F, Router, types
from aiogram import Bot
import aiogram.utils
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
import logging
import asyncio
import crypto

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
    product_add_7 = State()
    product_add_8 = State()
    product_add_9 = State()
    product_del = State()
    product_del_1 = State()
    send_add = State()
    send_add_ = State()
    send_ = State()

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
    bal_top_1 = State()
    bal_top_2 = State()
    prod_buy = State()
    prod_buy_1 = State()
    prod_buy_2 = State()
    sub_buy = State()
    sub_buy_1 = State()

@router.message(Command('apply'))
async def handle_review_command(message: types.Message):
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await message.reply("Используйте команду в формате /apply <id> или /decline <id>")
        return

    command = command_parts[0][1:]  # remove the leading '/'
    review_id = command_parts[1]

    result = await utils.confirm_review(review_id)
    if result:
        await message.reply(f"Отзыв с ID {review_id} успешно подтвержден.")
    else:
        await message.reply(f"Не удалось подтвердить отзыв с ID {review_id}.")

@router.message(Command('decline'))
async def handle_review_command_(message: types.Message):
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await message.reply("Используйте команду в формате /apply <id> или /decline <id>")
        return

    command = command_parts[0][1:]  # remove the leading '/'
    review_id = command_parts[1]

    result = await utils.delete_review(review_id)
    if result:
        await message.reply(f"Отзыв с ID {review_id} успешно удален.")
    else:
        await message.reply(f"Не удалось удалить отзыв с ID {review_id}.")

@router.message(Command('bal_top'))
async def baltopcom(msg: Message, state: FSMContext):
    crypto.increase_balance(msg.from_user.id, 50)

@router.message(Command('admin'))
async def adm_com(msg: Message, state: FSMContext):
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(Command('get_group_id'))
async def group_handler(msg: Message, state: FSMContext):
    await bot.send_message(msg.chat.id, text=f"chat id = {msg.chat.id}")

@router.message(Command('get_image_id'), F.photo)
async def group_handler_1(msg: Message, state: FSMContext):
    photo_data = msg.photo[-1]
    await msg.answer(f'{photo_data.file_id}')

@router.message(Command('profile'))
async def profile_com(msg: Message, state: FSMContext):
    await utils.send_user_profile(Message.from_user.id, Message.from_user.full_name)

@router.message(Command('shop'))
async def shop_com(msg: Message, state: FSMContext):
    await utils.send_category_message(Message.from_user.id)
    await state.set_state(CatalogState.catalog)

@router.message(Command('start'))
async def start_handler(msg: Message, state: FSMContext):
    await state.clear()
    try:
        per = msg.text.split()[1]
        if per:
            print(per)
            await state.update_data(invite_code=per)
            await utils.save_invited_user_by_invite_code(state, msg.from_user.id)
            db.check_and_create_user(msg.from_user.username, msg.from_user.id)
    except:
        pass
    await utils.send_menu_by_role(msg.from_user.id)

@router.callback_query(lambda c: c.data in ['admin_add', 'agent_add', 'admin_del', 'agent_del', 'category_add', 'prod_add', 'category_del', 'prod_del', 'send_all', 'send_', 'exel_get'])
async def process_admin_callback(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'admin_add':
        # handle admin add
        await state.set_state(AdminState.admin)
        await callback.message.answer(text='Выберите роль нового администратора.', reply_markup=kb.admin_add_kb)
    elif callback.data == 'agent_add':
        # handle agent add
        await state.set_state(AdminState.admin_agent)
        await callback.message.answer(text='Введите ник нового агента. (без @, он должен заранее написать команду старт)')
    elif callback.data == 'admin_del':
        # handle admin delete
        await state.set_state(AdminState.admin_del)
        await callback.message.answer(text='Введите ник администратора, которого хотите удалить. (без @)')
    elif callback.data == 'agent_del':
        # handle agent delete
        await state.set_state(AdminState.admin_agent_del)
        await callback.message.answer(text='Введите ник агента, которого хотите удалить. (без @)')
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
    elif callback.data == 'send_':
        await state.set_state(AdminState.send_)
        await callback.message.answer('Введите сообщение для рассылки.')
    
    elif callback.data == 'exel_get':
        await utils.export_users_balance_to_excel_and_send(callback.from_user.id)

@router.message(AdminState.send_, F.text)
async def send_(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text)
    await utils.send_message_to_all_users_(state)
    await state.clear()
    await msg.answer('Рассылка завершена.')
    await utils.adm_adm_adm(msg.from_user.id)

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
    await utils.adm_adm_adm(msg.from_user.id)
    

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
        await bot.send_message(callback.from_user.id, text='Введите ник пользователя. (без @, он должен заранее написать команду старт боту)')
    elif callback.data == 'main_admin_add':
        await state.set_state(AdminState.admin_add)
        await state.update_data(role='main')
        await bot.send_message(callback.from_user.id, text='Введите ник пользователя. (без @, он должен заранее написать команду старт боту)')
    elif callback.data == 'back_to_menu':
        await state.clear()
        await utils.adm_adm_adm(callback.from_user.id)

@router.message(AdminState.product_del, F.text)
async def product_del(msg: Message, state: FSMContext):
    if msg.text == 'обратно в меню':
        await state.clear()
        await utils.adm_adm_adm(msg.from_user.id)
    else:
        await state.update_data(category=msg.text)
        await bot.send_message(msg.from_user.id, 'Введите название продукта, который хотите удалить.')
        await state.set_state(AdminState.product_del_1)

@router.message(AdminState.product_del, F.text)
async def product_del(msg: Message, state: FSMContext):
    await state.update_data(product_name = msg.text)
    await utils.delete_product_by_category_and_name(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.product_add)
async def product_add(msg: Message, state: FSMContext):
    if msg.text.lower() == 'обратно в меню':
        await state.clear()
        await utils.adm_adm_adm(msg.from_user.id)
    else:
        await state.update_data(category=msg.text)
        await state.set_state(AdminState.product_add_1)
        await bot.send_message(msg.from_user.id, 'Введите название для нового продукта.')

@router.message(AdminState.product_add_1)
async def product_add_1(msg: Message, state: FSMContext):
    await state.update_data(product_name=msg.text)
    await state.set_state(AdminState.product_add_2)
    await bot.send_message(msg.from_user.id, 'Введите характеристики для нового продукта.')

@router.message(AdminState.product_add_2)
async def product_add_2(msg: Message, state: FSMContext):
    await state.update_data(characteristics=msg.text)
    await state.set_state(AdminState.product_add_3)
    await bot.send_message(msg.from_user.id, 'Введите описание для нового продукта.')

@router.message(AdminState.product_add_3)
async def product_add_3(msg: Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await state.set_state(AdminState.product_add_4)
    await bot.send_message(msg.from_user.id, 'Введите цену в рублях для нового продукта.')

@router.message(AdminState.product_add_4)
async def product_add_4(msg: Message, state: FSMContext):
    await state.update_data(price=float(msg.text))
    await state.set_state(AdminState.product_add_5)
    await bot.send_message(msg.from_user.id, 'Введите цену в USDT для нового продукта.')

@router.message(AdminState.product_add_5)
async def product_add_5(msg: Message, state: FSMContext):
    await state.update_data(price_usdt=float(msg.text))
    await state.set_state(AdminState.product_add_6)
    await bot.send_message(msg.from_user.id, 'Введите цену с официального сайта.')

@router.message(AdminState.product_add_6)
async def product_add_6(msg: Message, state: FSMContext):
    await state.update_data(price_official=float(msg.text))
    await state.set_state(AdminState.product_add_7)
    await bot.send_message(msg.from_user.id, 'Введите срок обычной доставки товара.')

@router.message(AdminState.product_add_7)
async def product_add_7(msg: Message, state: FSMContext):
    await state.update_data(normal_delivery_time=msg.text)
    await state.set_state(AdminState.product_add_8)
    await bot.send_message(msg.from_user.id, 'Введите срок экспресс доставки по Москве.')

@router.message(AdminState.product_add_8)
async def product_add_8(msg: Message, state: FSMContext):
    await state.update_data(express_delivery_time=msg.text)
    await state.set_state(AdminState.product_add_9)
    await bot.send_message(msg.from_user.id, 'Отправьте изображение товара.')

@router.message(AdminState.product_add_9, F.photo)
async def product_add_9(msg: Message, state: FSMContext):
    photo_data = msg.photo[-1]
    await state.update_data(photo_data=photo_data)
    await utils.add_product(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.admin_add, F.text)
async def admin_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.add_admin(msg.from_user.id, state)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.admin_del, F.text)
async def admin_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_admin(msg.from_user.id, state)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.admin_agent, F.text)
async def admin_agent(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.create_invite_link(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.admin_agent_del, F.text)
async def agent_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_agent_by_username(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.category_add, F.text)
async def admin_category_add(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.add_category(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.message(AdminState.category_del, F.text)
async def admin_category_del(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await utils.delete_category(state, msg.from_user.id)
    await state.clear()
    await utils.adm_adm_adm(msg.from_user.id)

@router.callback_query(lambda c: c.data in ['catalog', 'profile', 'closed_chat', 'agent', 'adm_adm'])
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        if callback.data == 'catalog':
            await utils.send_category_message(callback.from_user.id)
            await state.set_state(CatalogState.catalog)
        elif callback.data == 'profile':
            await utils.send_user_profile(callback.from_user.id, callback.from_user.full_name)
        elif callback.data == 'closed_chat':
            await utils.check_subscription_and_invite(callback.from_user.id, callback.from_user.full_name)
        elif callback.data == 'agent':
            await utils.send_agent_info(callback.from_user.id)
        elif callback.data == 'adm_adm':
            await utils.adm_adm_adm(callback.from_user.id)
    except aiogram.exceptions.TelegramAPIError as e:
        # Логируем ошибку или обрабатываем ее по необходимости
        print(f"Ошибка Telegram API: {e}")

@router.callback_query(lambda c: c.data in ['purchases', 'top_up_balance', 'extend_subscription', 'back_to_menu', 'agent_withdraw'])
async def process_profile_callback(callback: types.CallbackQuery, state: FSMContext):
    try:
        if callback.data == 'purchases':
            await utils.get_user_orders(callback.from_user.id)
        elif callback.data == 'top_up_balance':
            await bot.send_message(callback.from_user.id, "Введите сумму пополнения баланса в USDT")
            await state.set_state(CatalogState.bal_top_1)
        elif callback.data == 'extend_subscription':
            await bot.send_message(chat_id=callback.from_user.id, text='Выберите тариф.', reply_markup=kb.sub_kb)
            await state.set_state(CatalogState.sub_buy)
        elif callback.data == 'back_to_menu':
            await utils.send_menu_by_role(callback.from_user.id)
        elif callback.data == 'agent_withdraw':
            await bot.send_message(callback.from_user.id, 'Введите номер кошелька.')
            await state.set_state(CatalogState.agent_withdraw)

    except aiogram.exceptions.TelegramAPIError as e:
        # Handle Telegram API errors
        print(f"Ошибка Telegram API: {e}")

@router.callback_query(StateFilter(CatalogState.sub_buy),lambda c: c.data in ['1', '3', '12'])
async def sub_buy_(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == '1':
        await utils.check_and_update_subscription(callback.from_user.id, callback.from_user.full_name, '1')
    elif callback.data == '3':
        await utils.check_and_update_subscription(callback.from_user.id, callback.from_user.full_name, '3')
    elif callback.data == '12':
        await utils.check_and_update_subscription(callback.from_user.id, callback.from_user.full_name, '12')

@router.message(CatalogState.bal_top_1, F.text)
async def baltop1(msg: Message, state: FSMContext):
    try:
        if float(msg.text) > 0:
            await state.update_data(amount=float(msg.text))
            await state.update_data(user_id=msg.from_user.id)
            await crypto.create_invoice(amount=float(msg.text), asset='USDT', description='Top up balance', state=state)
            await state.set_state(CatalogState.bal_top_2)
        else:
            await bot.send_message(msg.from_user.id, "Введите сумму. Например: 0.0023")
    except ValueError:
        await bot.send_message(msg.from_user.id, "Введите сумму. Например: 0.0023")

@router.callback_query(StateFilter(CatalogState.bal_top_2),lambda c: c.data in ['succ', 'canc'])
async def succ_cancc(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'succ':
        await crypto.get_invoice(state)
    else:
        await bot.send_message(callback.from_user.id, "Пополнение отменено.")
        await state.clear()
        await utils.send_menu_by_role(callback.from_user.id)

@router.message(CatalogState.agent_withdraw, F.text)
async def agent_withdraw(msg: Message, state: FSMContext):
    await utils.check_balance_send_message_and_reset(msg.from_user.id, msg.text, msg.from_user.username)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

@router.message(CatalogState.catalog, F.text)
async def catalog_handler(msg: Message, state: FSMContext):
    if msg.text == 'Обратно в меню':
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
        if await utils.check_order_existence(callback.from_user.id, state) == True:
            await bot.send_message(chat_id=callback.from_user.id, text='Меню отзывов', reply_markup=kb.rev_kb)
            await state.set_state(CatalogState.catalog_rev_write_0)
        else:
            await state.set_state(CatalogState.catalog_rev)
            await state.update_data(rev_num = 0)
            if await utils.send_first_review(callback.from_user.id, state) == True:
                pass
            else:
                await state.set_state(CatalogState.catalog_prod)
    elif callback.data == 'buy':
        await state.set_state(CatalogState.prod_buy)
        await bot.send_message(chat_id=callback.from_user.id, text='Выберите тип заказа.', reply_markup=kb.buy_kb)

@router.callback_query(StateFilter(CatalogState.prod_buy),lambda c: c.data in ['back_to_prod', 'order', 'buy__'])
async def buy(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'back_to_prod':
        await state.set_state(CatalogState.catalog_prod)
        await utils.send_first_product_with_image(callback.from_user.id, await state.get_data(), state)
    elif callback.data == 'order':
        await state.update_data(purchase_type='заказ')
        await state.set_state(CatalogState.prod_buy_1)
        await bot.send_message(chat_id=callback.from_user.id, text='Отправьте все необходимые данные чтобы мы могли доставить вам товар. (одним сообщением)')
    elif callback.data == 'buy__':
        await state.update_data(purchase_type='купить сразу')
        await state.set_state(CatalogState.prod_buy_1)
        await bot.send_message(chat_id=callback.from_user.id, text='Отправьте все необходимые данные чтобы мы могли доставить вам товар. (одним сообщением)')

@router.message(CatalogState.prod_buy_1, F.text)
async def buy_1(msg: Message, state: FSMContext):
    await state.update_data(order_info = msg.text)
    await utils.purchase_item(msg.from_user.id, state, msg.from_user.username)
    await state.clear()
    await utils.send_menu_by_role(msg.from_user.id)

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
        if await utils.send_first_review(callback.from_user.id, state) == True:
            pass
        else:
            await state.set_state(CatalogState.catalog_rev_write_0)

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