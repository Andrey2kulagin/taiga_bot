import requests


def get_auth_refresh_via_username(domain: str, username: str, password: str) -> tuple[int, str]:
    endpoint = "api/v1/auth"
    data = {
        "type": "normal",
        "username": username,
        "password": password
    }
    response = requests.post(url=domain+endpoint, data=data)
    status_code = response.status_code
    response_data = response.json()
    auth_token = response_data.get("auth_token")
    refresh = response_data.get("refresh")
    return status_code, auth_token, refresh




def list_projects(auth_token):
    print("auth_token", auth_token)
    endpoint = f"api/v1/projects"
    refresh = ""
    data = {
        "description": "Beta description",
        "name": "Beta project"
    }
    headers = {
        "Authorization": f"Application {auth_token}"
        
    }
    response = requests.post(url=domain+endpoint, headers=headers, data=data)
    print(response.status_code)
    print(response.json())


def get_application_auth_code(application_id, auth_token, domain):
    get_endpoint = f"api/v1/applications/{application_id}/token"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    get_response = requests.get(url=domain+get_endpoint, headers=headers)
    status_code = get_response.status_code
    print("our_status = ", status_code)
    if status_code != 200:
        return 500, ""
    auth_code = get_response.json().get("auth_code")
    if auth_code is None:
        print("TUT")
        #генерируем новый
        token_gen_endpoint = f"api/v1/application-tokens/authorize"
        data = {
            "application": application_id,
        }
        response = requests.post(url=domain+token_gen_endpoint, data=data, headers=headers)
        status_code = response.status_code
        if status_code != 200:
            return 500, ""
        auth_code = response.json().get("auth_code")
    return 200, auth_code


def get_application_token(application_id, auth_token, domain):
    # здесь устанавливается токен для пользователя приложения. Его надо потом ещё активировать
    status, application_auth_code = get_application_auth_code(application_id, auth_token, domain)
    if status != 200:
        return 500, ""
    endpoint = f"api/v1/application-tokens/validate"
    data = {
        "application": application_id,
        "auth_code": application_auth_code,
    }
    headers = {

        "Authorization": f"Bearer {auth_token}"
    }
    response = requests.post(url=domain+endpoint, data=data, headers=headers)
    if response.status_code == 200:
        return 200, response.json().get("token")
    return 500, ""
    

    

def get_application_ver_token(username: str, password: str, application_id: str, domain: str) -> str:
    # получаем auth_token
    status_code, auth_token, refresh = get_auth_refresh_via_username(
        domain, username, password)
    if status_code == 200:
        # получаем токен и верифицируем токе
        return get_application_token(application_id, auth_token, domain)
    else:
        return 401, "Неправильные логин или пароль или такого пользователя не существует"
    


if __name__ == "__main__":
    domain = "http://127.0.0.1:9000/"
    status, token = get_application_ver_token("admin", "12345", "76212bb2-5378-4839-bb85-1b26ec408dfa", "http://127.0.0.1:9000/")

    list_projects("eyJhcHBfdG9rZW5faWQiOjR9:1qpoCG:ue-62-rvrOwkfl4TEIg41f8WybDSiGG4iA_wEVqXo94")
