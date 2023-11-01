import requests


def create_webhook(auth_token: str, key: str, name: str, project_id: int, url_webhook: str) -> dict:
    url_t = "https://api.taiga.io/api/v1/webhooks"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    webhook_data = {
        "key": key,
        "name": name,
        "project": project_id,
        'url': url_webhook
    }

    response = requests.post(url_t, json=webhook_data, headers=headers)

    if response.status_code == 201:
        print("Webhook успешно создан.")
        webhook_detail = response.json()
        return webhook_detail
    else:
        print(f"Ошибка {response.status_code}: Не удалось создать webhook.")
        return None
