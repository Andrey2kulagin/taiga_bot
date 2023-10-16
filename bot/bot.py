import urllib.parse
from pyrogram import Client, filters
from urllib.parse import urlparse
from bot_config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton, CallbackQuery)

# Если работать не будет, то убрать асинк нафиг
# словарь для хранения состояний пользователей
user_states = {}

# url инстанса тайги для каждого пользователя
taiga_instances_urls = {}

# url страницы авторизации на бэкенде
authorization_page_url = "http://127.0.0.1:8000/"

# Создание экземпляра нового клиента
app = Client(
    "taigatestbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# Если пользователь начал диалог с ботом используя команду "/start",
# То вывести ему список команд
@app.on_message(filters.command("start"))
async def start(client, message):
    # устанавливаем начальное состояние пользователя
    user_states[message.chat.id] = "main_menu"

    keyboard = [
        ["login", "etc"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    # TODO: проверить на существующую интеграцию в боте. Если авторизован, то показать кнопку выхода вместо кнопки
    #  входа
    await message.reply(
        "This is Taiga integration bot.\n"
        "It can notify you about events in your projects.\n"
        "You can also use it to create an issue.",
        reply_markup=reply_markup
    )


# Если пришло сообщение от пользователя и его сотояние - главное меню
@app.on_message(filters.text)
async def menu_handler(client, message):
    state = user_states.get(message.chat.id)

    # http://127.0.0.1:8000/login/standard?domain=домен&tg_id=1257343
    async def send_auth_link():
        url = {
            "domain": str(taiga_instances_urls.get(message.chat.id)),
            "tg_id": str(message.chat.id)
        }
        await message.reply(
            "To authorize, please follow this link: \n" +
            authorization_page_url + "login/standard?" + urllib.parse.urlencode(url, safe='') + "\n\n" +
            "To authorize using application token, please follow this link: " +
            authorization_page_url + "login/application?" + urllib.parse.urlencode(url, safe='')
        )

    if message.text == "login":
        user_states[message.chat.id] = "choosing_instance"
        await message.reply(
            "Choose your Taiga instance",
            reply_markup=ReplyKeyboardMarkup(
                [
                    ["taiga.io (default)", "Custom instance"]  # Первый ряд кнопок
                ],
                one_time_keyboard=True,
                resize_keyboard=True  # Make the keyboard smaller
            )
        )

    if state == "choosing_instance":
        if message.text == "Custom instance":
            user_states[message.chat.id] = "setting_custom_instance_url"
            await message.reply(
                "Write your taiga instance URL:"
            )
        if message.text == "taiga.io (default)":
            taiga_instances_urls[message.chat.id] = "https://taiga.io"
            user_states[message.chat.id] = "authorizing"
            await send_auth_link()

    if state == "setting_custom_instance_url":
        # TODO: проверки на валидность URL
        # TODO: ОБЯЗАТЕЛЬНО сделать защиту от XSS
        taiga_instances_urls[message.chat.id] = message.text
        user_states[message.chat.id] = "authorizing"
        await send_auth_link()


# Automatically start() and idle()
app.run()
