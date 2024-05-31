from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio, logging
import sqlite3
import time

db = sqlite3.connect('.\PILLS_database\PILLS\database.db')
def get_pill_info(age_group):
        cursor = db.cursor()
        if age_group == 'Взрослый':
            query = f"SELECT dosage, doses_per_day FROM adults WHERE adults.id = id"
        else: query = f"SELECT dosage, doses_per_day FROM kids WHERE kids.id = id"
        cursor.execute(query)
        return cursor.fetchone()

def get_buy_info(pills_name):
    cursor = db.cursor()
    query = f"SELECT link FROM pills WHERE pills.name = name"
    cursor.execute(query)
    return cursor.fetchone()


API_TOKEN = '7036140386:AAEMCWevUvtoeMInDiCi7opdtM_1UerPPgc'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


user_age = {}  # переменная для хранения информации о возрасте пользователя
awaiting_record_info = {}


@dp.message(Command('start'))
async def start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f"Привет, {user_name}! Я бот-напоминалка. Можешь написать /help для вывода списка команд. Для начала работы, давай определимся с твом возрастом. Напиши /age для ответа.")

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
    user_age[message.from_user.id] = message.text
    cursor = db.cursor()
    query = f"""INSERT INTO users(telegram_id, age) 
                        VALUES("{message.from_user.id}", "{message.text}")"""
    cursor.execute(query)
    db.commit()
    await message.reply("Отлично! Теперь напиши /record <название таблетки> <количество дней курса>, чтобы запустить систему напоминаний!", reply_markup=types.ReplyKeyboardRemove())
    # await state.finish()


@dp.message(Command('record'))
async def record_pill(message: types.Message):
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Пожалуйста, введите команду в формате /record <название таблетки> <кол-во дней курса>.")
        return

    pill_name = args[1:-1]
    try:
        days = int(args[-1])
    except ValueError:
        await message.reply("Количество дней курса должно быть числом.")
        return

    user_id = message.from_user.id
    age_group = user_age[user_id]
    pill_info = get_pill_info(age_group)

    if not pill_info:
        await message.reply("Препарат не найден. Пожалуйста, проверьте название препарата и попробуйте снова.")
        return

    dosage, doses_per_day = pill_info
    awaiting_record_info[user_id] = (pill_name, dosage, doses_per_day, days)

    # Создание кнопок подтверждения
    kb_confirm = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, все верно", callback_data="confirm_yes")],
        [InlineKeyboardButton(text="Нет, хочу изменить", callback_data="confirm_no")]
    ])

    await message.reply(
        f"Препарат: {' '.join(pill_name)}, дозировка: {dosage}, приемов в день: {doses_per_day}, количество дней приема: {days}. Все верно?",
        reply_markup=kb_confirm)


@dp.callback_query(lambda c: c.data.startswith('confirm_'))
async def process_confirm(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    if callback_query.data == "confirm_yes":
        if user_id in awaiting_record_info:
            pill_name, dosage, doses_per_day, days = awaiting_record_info[user_id]
            await callback_query.message.edit_text("Напоминания успешно установлены!")
            del awaiting_record_info[user_id]
            for i in range(days):
                time.sleep(3)
                #time.sleep(86400/doses_per_day)
                msg='Пора принимать '+str(' '.join(pill_name))
                await bot.send_message(user_id, msg)
        else:
            await callback_query.message.edit_text("Произошла ошибка. Попробуйте снова.")

    elif callback_query.data == "confirm_no":
        await callback_query.message.edit_text("Пожалуйста, введите команду /record снова.")
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


@dp.message(Command('buy'))
async def buy_pill(message: types.Message):
    args = message.text.split()
    pill_name = args[1:]
    buy_info = get_buy_info(' '.join(args))
    await message.reply("Вы можете купить "+ ' '.join(pill_name)+" здесь: "+ str(''.join(buy_info)))


@dp.message(Command('help'))
async def help(message: types.Message):
    await message.reply("/start перезапускает бота\n/age позволяет выбрать возраст\n/record записывает новое напоминание\n/buy присылает ссылку на страницу лекарства в аптеке")



if __name__ == '__main__':
    asyncio.run(main())
