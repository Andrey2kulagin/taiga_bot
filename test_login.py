import requests

domain = "https://api.taiga.io/"

def basic_login():
    endpoint = "api/v1/auth"
    data = {
        "password": "",
        "type": "normal",
        "username": "andrey2kulagin@yandex.ru"
    }
    response = requests.post(url=domain+endpoint, data=data)
    print(response.status_code)
    print(response.json())

def get_github_access_token(github_key):
    github_url = "https://github.com/login/oauth/access_token"
    github_data = {
        "client_id": "",
        "client_secret":"", 
        "code": github_key
    }
    headers = {
    "Accept": "application/json"
    }
    github_resp = requests.post(url=github_url, data=github_data, headers=headers)
    print(github_resp.status_code)
    print(github_resp)
    print(github_resp.json())


def github_login(github_token):
    endpoint = "api/v1/auth"
    data = {
        "type": "github",
        "code": github_token
    }
    
    response = requests.post(url=domain+endpoint, data=data)
    print(response.status_code)
    print(response.json())


def get_for_refresh():
    endpoint = "api/v1/auth/refresh"
    refresh = ""
    data = {
        "refresh": refresh
    }
    headers = {
    "Content-Type": "application/json"
    }
    response = requests.post(url=domain+endpoint,data=data)
    print(response.status_code)
    print(response.json())

if __name__=="__main__":
    github_login("")
    #get_github_access_token("")
