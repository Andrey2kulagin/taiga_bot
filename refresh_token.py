import requests


def refresh_access_token(refresh_token: str) -> tuple[int, dict]:
    # URL и заголовки для запроса
    url = "https://api.taiga.io/api/v1/auth/refresh"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "refresh": refresh_token
    }

    # Отправляем POST-запрос
    response = requests.post(url, headers=headers, json=data)

    return response.status_code, response.json()
