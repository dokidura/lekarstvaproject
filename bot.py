from aiogram import Bot, Dispatcher, types
import asyncio
import logging
import time

TOKEN = '7036140386:AAFroHSqNQzfBKprVWZf8m9kro4XoQM9dFo'
MSG = 'Напоминание о приеме таблеток!'

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def echo_message(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.answer(f"Привет, {user_full_name}!")

    for i in range(3):
        time.sleep(3)
        await bot.send_message(user_id, MSG)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

