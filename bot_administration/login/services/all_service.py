import requests

def get_auth_refresh_via_username(domain: str, username: str, password: str) -> tuple[int, str]:
    print(domain)
    endpoint = "api/v1/auth"
    data = {
        "type": "normal",
        "username": username,
        "password": password
    }
    response = requests.post(url=domain+endpoint, data=data)
    status_code = response.status_code
    print(status_code)
    if status_code == 200:
        response_data = response.json()
        auth_token = response_data.get("auth_token")
        refresh = response_data.get("refresh")
        return status_code, auth_token, refresh
    return status_code, "wrr", "wee"