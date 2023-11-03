import requests


def list_project(auth_token, member_id):
    auth_token = auth_token
    url = f"https://api.taiga.io/api/v1/projects?member={member_id}&order_by=user_order&slight=true"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        projects_info = [{"id": project["id"], "name": project["name"]} for project in data]
        return projects_info
    else:
        return f"Ошибка: {response.status_code}"
