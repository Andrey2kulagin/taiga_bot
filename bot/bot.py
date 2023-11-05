import urllib.parse
from pyrogram import Client, filters
import re
from bot_config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,
                            InlineKeyboardButton,ReplyKeyboardRemove, CallbackQuery)
from db_worker import BotUserSettings, LoginBotUser
from lists_project import list_project
from token_parse import parse_user_id
from refresh_token import refresh_access_token_by_tg_id

# TODO: использовать бд вместо этого
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
async def start_command_handler(client, message):
    # устанавливаем начальное состояние пользователя
    await BotUserSettings.write_botuser_state(message.chat.id, "main_menu")
    # если пользователь авторизован в тайге
    if await LoginBotUser.is_botuser_logged_in(message.chat.id):
        # устанавливаем состояние logged_in (зачем??)
        await BotUserSettings.write_botuser_state(message.chat.id, "logged_in")
        # Рисуем клавиатуру авторизованного пользователя с кнопками списка, isuues и выхода из аккаунта
        # TODO: выводить эту клавиатуру после того как отдали пользователю ссылки на авторизацию
        keyboard = [
            ["/projects", "/issues", "/logout"]
        ]
    # иначе, если авторизация не произведена, то клавиатура с одной командой - для входа
    else:
        keyboard = [
            ["/login"]
        ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await message.reply(
        "This is Taiga integration bot.\n"
        "It can notify you about events in your projects.\n"
        "You can also use it to create an issue.",
        reply_markup=reply_markup
    )


# TODO: убрать к чертям собачим, когда будет готово автоматическое обновление токенов
@app.on_message(filters.command("refresh_token"))
async def refresh_token_command_handler(client, message):
    result = await refresh_access_token_by_tg_id(message.chat.id)
    if result == 200:
        await message.reply("Token has been successfully refreshed")
    else:
        await message.reply("Refresh token is rotten or something else went wrong.\n"
                      "Try to log in again")


# Если пришло сообщение от пользователя с командой для вывода списка
@app.on_message(filters.command("projects"))
async def projects_command_handler(client, message):
    # если пользователь залогинен, то работаем
    if await LoginBotUser.is_botuser_logged_in(message.chat.id):
        token = await LoginBotUser.get_auth_token(message.chat.id)
        # этот скрипт возможно поменяет свое местоположение в какую-нибудь папку utils
        projects = list_project(token, await parse_user_id(token))
        if projects[0] == 200:
            msg = ''
            for i in range(len(projects[1])):
                msg += "**" + str(i+1) + ".** " + projects[1][i]["name"] + "\n"
            await message.reply(
                msg
            )
        else:
            await message.reply(
                projects[1]
            )
    # иначе облом
    else:
        # TODO: вынести в отдельную функцию, судя по всему это будет использоваться хуеву тучу раз
        keyboard = [
            ["/login"]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await message.reply(
            "You have to be logged in",
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
