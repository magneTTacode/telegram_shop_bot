import requests
import asyncio
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
import aiohttp
import kb
import text
import db
import config
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = Bot(token=config.BOT_TOKEN)

API_URL = 'https://testnet-pay.crypt.bot/'
API_TOKEN = '226413:AADHXnoZuJPKF60vCbCBEBUkOc7tFe9PVaB'

from aiocryptopay import AioCryptoPay, Networks
crypto = AioCryptoPay(token=API_TOKEN, network=Networks.MAIN_NET)

async def create_invoice(amount, asset, description, state):
    invoice = await crypto.create_invoice(asset=asset, amount=amount, description=description)

    invoice_id = invoice.invoice_id
    invoice_url = invoice.mini_app_invoice_url

    await state.update_data(invoice_id=invoice_id)
    await state.update_data(invoice_url=invoice_url)
    await state.update_data(amount=amount)
    keyb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="оплатить", url=invoice_url)
    ],
    [
        InlineKeyboardButton(text="Готово", callback_data="succ"),
        InlineKeyboardButton(text="Отмена", callback_data="canc"),
    ]
])
    data = await state.get_data()
    user_id = data['user_id']
    await bot.send_message(chat_id=user_id, text='Оплатите пополнение баланса.', reply_markup=keyb)

async def get_invoice(state):
    data = await state.get_data()
    user_id = data['user_id']
    invoice_id = data['invoice_id']
    amount = data['amount']
    invoice = await crypto.get_invoices(invoice_ids=invoice_id)

    print(invoice.status)

    if invoice.status == "paid":
        await bot.send_message(user_id, 'paid')
        increase_balance(user_id, amount)
    else:
        await bot.send_message(user_id, 'Оплата не была проведена.')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gq1ihzD1nVW20m50izf6',
    'database': "telegram_bot"
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

def increase_balance(user_id, amount):
    sql = "UPDATE profiles SET balance = balance + %s WHERE user_id = %s"
    val = (amount, user_id)
    cursor.execute(sql, val)
    conn.commit()
    print(cursor.rowcount, "запись обновлена")