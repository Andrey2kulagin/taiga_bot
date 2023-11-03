import requests


def create_issue(auth_token, assigned_to=None, blocked_note=None, description='',
                 due_date=None, is_blocked=None, is_closed=False, priority=3384696,
                 project=1111111, severity=5633961, status=7894612, subject='', tags=[], type=3391300):
    # Подготовка данных для создания задачи
    data = {
        "assigned_to": assigned_to,  # user id, кому поручаешь
        "description": description,  # string, описание issue
        "is_closed": is_closed,
        "priority": priority,  # id приоритета
        "project": project,  # id проекта
        "severity": severity,  # id серьёзности
        "status": status,  # id статуса
        "subject": subject,  # название issue
        "tags": tags,  # лист тегов
        "type": type  # id тайпа
    }

    if blocked_note is not None:
        data["blocked_note"] = blocked_note # reason why the issue is blocked, причина блока
    if due_date is not None:
        data["due_date"] = due_date # str с дедлайном
    if is_blocked is not None:
        data["is_blocked"] = is_blocked # boolean, блокировка

    # URL для отправки POST-запроса
    url = "https://api.taiga.io/api/v1/issues"

    # Заголовки для POST-запроса
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }

    # Отправляем POST-запрос
    response = requests.post(url, json=data, headers=headers)

    # Проверяем статус кода ответа
    if response.status_code == 201:
        print("Задача успешно создана!")
        issue_detail = response.json()  # Детали созданной задачи
        return issue_detail
    else:
        print("Не удалось создать задачу. HTTP статус код:", response.status_code)
        return None
