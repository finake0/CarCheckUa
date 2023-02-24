import re
import aiogram
import requests
from aiogram import Bot, Dispatcher, types
from aiogram import Bot, Dispatcher, executor, types

bot_token = '' #@Bot_Father

bot = Bot(token=bot_token)

dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Отправь мне гос.номер автомобиля 🇺🇦")

@dp.message_handler(lambda message: re.search(r'^[А-Я]{2}\d{4}[А-Я]{2}$', message.text))
async def search_car(message: types.Message):
    car_number = message.text.upper()

    key = "" # Апи-ключ на 1000 запросов - https://baza-gai.com.ua/api
    url = f"https://baza-gai.com.ua/nomer/{car_number}"
    headers = {"Accept": "application/json", "X-Api-Key": key}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        car_info = f"Номер: {data['digits']}\n"
        car_info += f"Марка: {data['vendor']} {data['model']}\n"
        car_info += f"Год выпуска: {data['model_year']}\n"
        car_info += f"Регион: {data['region']['name']} ({data['region']['name_ua']})\n"
        car_info += f"Цвет: {data['operations'][0]['color']['ru']} ({data['operations'][0]['color']['ua']})\n"
        await message.answer(car_info)
    else:
        await message.answer("Ошибка!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
