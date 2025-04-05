from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
import json
import os

API_TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

try:
    with open('users.json', 'r') as f:
        users = json.load(f)
except FileNotFoundError:
    users = {"users": []}

def save_data():
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def get_user(user_id, username):
    for user in users["users"]:
        if user["user_id"] == user_id:
            return user
    new_user = {
        "user_id": user_id,
        "username": username,
        "balance": 0,
        "click_power": 1
    }
    users["users"].append(new_user)
    save_data()
    return new_user

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Кликнуть"))
keyboard.add(KeyboardButton("Баланс"), KeyboardButton("Обменять"))
keyboard.add(KeyboardButton("Апгрейд"))

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    get_user(message.from_user.id, message.from_user.username)
    await message.answer("Добро пожаловать в iBombsh! Бомби на здоровье!", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == "Кликнуть")
async def click(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    user["balance"] += user["click_power"]
    save_data()
    await message.answer(f"Бабах! Ты получил {user['click_power']} $BOMBSH")

@dp.message_handler(lambda message: message.text == "Баланс")
async def balance(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    await message.answer(f"У тебя {user['balance']} $BOMBSH")

@dp.message_handler(lambda message: message.text == "Апгрейд")
async def upgrade(message: types.Message):
    user = get_user(message.from_user.id, message.from_user.username)
    user["click_power"] += 1
    save_data()
    await message.answer(f"Ты прокачался! Теперь за клик даётся {user['click_power']} $BOMBSH")

@dp.message_handler(lambda message: message.text == "Обменять")
async def exchange(message: types.Message):
    await message.answer("Скоро ты сможешь обменять $BOMBSH на гравитацию и мемы. Следи за апдейтами.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
