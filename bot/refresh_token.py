import requests
from db_worker import LoginBotUser
import asyncio


async def refresh_access_token(refresh_token: str) -> tuple[int, dict]:
    # URL и заголовки для запроса
    # TODO: сделать URL динамически определяемым
    url = "https://api.taiga.io/api/v1/auth/refresh"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "refresh": refresh_token
    }

    # Отправляем POST-запрос
    response = requests.post(url, headers=headers, json=data)
    print(response.status_code, response.json())

    if response.status_code == 200:
        # жсон по переменным
        auth_token = response.json()['auth_token']
        new_refresh_token = response.json()['refresh']
        print(new_refresh_token)
        # отдаем методу которая колупает базу даных все токены что имеем, чтобы она из заменила
        await LoginBotUser.update_tokens(refresh_token, new_refresh_token, auth_token)

    return response.status_code, response.json()


async def refresh_access_token_by_tg_id(tg_id):
    refresh_token = await LoginBotUser.get_refresh_token(tg_id)
    result = await refresh_access_token(refresh_token)
    return result[0]


# async def main():
#     print(await refresh_access_token(
#             "token"
#         )
#     )
#
#
# if __name__ == '__main__':
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(main())
#     loop.close()
