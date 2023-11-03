import requests
from .all_service import get_auth_refresh_via_username, create_tg_user
from django.http import Http404

def get_application_auth_code(application_id, auth_token, domain):
    get_endpoint = f"api/v1/applications/{application_id}/token"
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    get_response = requests.get(url=domain+get_endpoint, headers=headers)
    status_code = get_response.status_code
    if status_code != 200:
        if status_code == 404:
            raise Http404("Неверный id приложения")
        return status_code, "" # может быть 404
    auth_code = get_response.json().get("auth_code")
    if auth_code is None:
        #генерируем новый
        token_gen_endpoint = f"api/v1/application-tokens/authorize"
        data = {
            "application": application_id,
        }
        response = requests.post(url=domain+token_gen_endpoint, data=data, headers=headers)
        status_code = response.status_code
        if status_code != 200:
            return status_code, ""
        auth_code = response.json().get("auth_code")
    return 200, auth_code


def get_application_token(application_id, auth_token, domain):
    # здесь устанавливается токен для пользователя приложения. Его надо потом ещё активировать
    status, application_auth_code = get_application_auth_code(application_id, auth_token, domain)
    if status != 200:
        return status, ""
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
    return response.status_code, ""
    

    

def get_application_ver_token(username: str, password: str, application_id: str, domain: str) -> str:
    # получаем auth_token
    status_code, auth_token, refresh = get_auth_refresh_via_username(
        domain, username, password)
    if status_code == 200:
        # получаем токен и верифицируем токе
        return get_application_token(application_id, auth_token, domain)
    else:
        return 401, "Неправильные логин или пароль или такого пользователя не существует"


def application_login_handler(username, password, application_id, domain, tg_id):
    try:
        status, token = get_application_ver_token(username, password, application_id, domain)
        if status == 200:
            create_tg_user(tg_id=tg_id, domain=domain,auth_type="Application",application_token=token)
            return status, ""
        return status, token
    except Http404:
        return 404, "Приложения с таким id нет"