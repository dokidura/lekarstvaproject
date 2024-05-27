from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
import asyncio, logging
import sqlite3

API_TOKEN = '7036140386:AAEMCWevUvtoeMInDiCi7opdtM_1UerPPgc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

db = sqlite3.connect('.\PILLS_database\PILLS\database.db')


user_age = {}  # переменная для хранения информации о возрасте пользователя

@dp.message(Command('start'))
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! Я бот-напоминалка. Для начала работы, давай определимся с твом возрастом. Напиши /age для ответа.")

@dp.message(Command('age'))
async def ask_age(message: types.Message):
    kb = [
            [types.KeyboardButton(text="Взрослый")],
            [types.KeyboardButton(text="Ребенок")]
        ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Ты взрослый или ребенок?", reply_markup=keyboard)

@dp.message(lambda message: message.text in ["Взрослый", "Ребенок"])
async def save_age(message: types.Message):
    cursor = db.cursor()
    query = f"""INSERT INTO users(telegram_id, age) 
                        VALUES("{message.from_user.id}", "{message.text}")"""
    cursor.execute(query)
    db.commit()
    await message.reply("Отлично! Теперь напиши /record <название таблетки> <количество дней курса>, чтобы запустить систему напоминаний!", reply_markup=types.ReplyKeyboardRemove())
    # await state.finish()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())