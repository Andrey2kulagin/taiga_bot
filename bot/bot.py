import urllib.parse
from pyrogram import Client, filters
import re
from bot_config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton,ReplyKeyboardRemove, CallbackQuery)
from db_worker import BotUserSettings, LoginBotUser

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
    await BotUserSettings.write_botuser_state(message.chat.id, "main_menu")
    # TODO: убрать дубликаты
    if await LoginBotUser.is_botuser_logged_in(message.chat.id):
        await BotUserSettings.write_botuser_state(message.chat.id, "logged_in")
        await message.reply(
            "This is Taiga integration bot.\n"
            "It can notify you about events in your projects.\n"
            "You can also use it to create an issue."
        )
        await message.reply(
            "You already logged in",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        keyboard = [
            ["/login", "/etc"]
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
    state = await BotUserSettings.read_botuser_state(message.chat.id)
    if message.text == "/login":
        if await LoginBotUser.is_botuser_logged_in(message.chat.id):
            await BotUserSettings.write_botuser_state(message.chat.id, "logged_in")
            await message.reply(
                "You already logged in",
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await BotUserSettings.write_botuser_state(message.chat.id, "choosing_instance")
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
            await BotUserSettings.write_botuser_state(message.chat.id, "setting_custom_instance_url")
            await message.reply(
                "Write your taiga instance URL in `https://api.example.com` format:"
            )
        # TODO: перезапустить бота после того как отдал ссылки
        if message.text == "taiga.io (default)":
            taiga_instances_urls[message.chat.id] = "https://api.taiga.io"
            await BotUserSettings.write_botuser_state(message.chat.id, "authorizing")

            # http://127.0.0.1:8000/login/standard?domain=домен&tg_id=1257343
            url = {
                "domain": str(taiga_instances_urls.get(message.chat.id)),
                "tg_id": str(message.chat.id)
            }
            direct_auth = authorization_page_url + "login/standard?" + urllib.parse.urlencode(url, safe='')
            gh_auth = authorization_page_url + "login/application?" + urllib.parse.urlencode(url, safe='')
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Login", url=direct_auth)],
                    [InlineKeyboardButton("Login via GitHub", url=gh_auth)]
                ]
            )
            await message.reply("To authorize, please follow one of these links:", reply_markup=keyboard)

    if state == "setting_custom_instance_url":
        # TODO: ОБЯЗАТЕЛЬНО сделать защиту от XSS
        msg = message.text
        # https://stackoverflow.com/questions/7160737/
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if re.match(url_regex, msg):
            taiga_instances_urls[message.chat.id] = msg
            await BotUserSettings.write_botuser_state(message.chat.id, "authorizing")
            # http://127.0.0.1:8000/login/standard?domain=домен&tg_id=1257343
            url = {
                "domain": str(taiga_instances_urls.get(message.chat.id)),
                "tg_id": str(message.chat.id)
            }
            direct_auth = authorization_page_url + "login/standard?" + urllib.parse.urlencode(url, safe='')
            gh_auth = authorization_page_url + "login/application?" + urllib.parse.urlencode(url, safe='')
            keyboard = InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("Login", url=direct_auth)],
                    [InlineKeyboardButton("Login via app key", url=gh_auth)]
                ]
            )
            await message.reply("To authorize, please follow one of these links:", reply_markup=keyboard)
        # elif (msg == "taiga.io") or (msg == "https://taiga.io") or (msg == "https://api.taiga.io")
        else:
            await message.reply("Invalid url, try again using right format (`https://api.example.com`)")


# Automatically start() and idle()
app.run()
