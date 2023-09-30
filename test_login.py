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

def get_application_id():
    endpoint = "api/v1/application-tokens"
    bearer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjk2MDg4NDQ3LCJqdGkiOiIxN2IwNDZhOGJmYTc0ZmQ2ODNkZGFlOTg2ZjgwMzNiNiIsInVzZXJfaWQiOjU5MzAyNn0.EUYGlLvSTifVyfjJlAZqq81i7-sKB9jHQ-c1NSPJ5H7OuWrDie1teD-H0aiLAxywlXZ1aeyADWRHXJVkH68w6sLy_dFtG9W-CMJsDznRmaDEFGF_fv9JfCxk81ABFYcaFijKrsKY-kkZOATO01BuXAGnkuZnllLzyMB98amr7Htjyihk34l5xSCiFHNnHUoZAblolrdvTPO0c93cbvCwM1XyV0er2OCZrecajjbterGl9vLko_oHC8nGYBtPoDFNfb1SthgK-2O1kZiWYa3rIM23Oej0MiS8usLBVTCDxXuIu99L0eJEVYtEEZrbe35KWqnzqWVHqdsv2_A-OmSGrQ"
    headers = {
    'Authorization': f'Bearer {bearer_token}',
    "Content-Type": "application/json"
    }
    response = requests.get(url=domain+endpoint, headers=headers)
    print(response.status_code)
    print(response.json())

def get_for_refresh():
    endpoint = "api/v1/auth/refresh"
    refresh = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5NjM1MDI1MywianRpIjoiOWRlY2RkMmFmYmFkNDUzMTk5MTJlNjViOWQ5YzNkMzgiLCJ1c2VyX2lkIjo1OTMwMjZ9.ecdVkYI80ShhomatuBTJnSHEeN2zeB0TN_312rHbj-RarUVJkA7wj6IYa6OvWFWcSCXkgHXYqzz8BbGcaLf_-QylAxh5ZoyH38BGUMTu-iJBpp4hZVOxIvw0GvspwK2BWIERHCgyW5GmQiXXeR9p5LygqE1YvTV-CRVGyw-6UkREImpCy0pltjl6sL79Fwg8AiDu57d3WL8cqpD7wZ6j_hAuyXMDlI_xaJmB3pZ5uhJJXFaVa8M2mt4C4TRhR0-Nd4IWqzGFUtaATxPlV003lyBYoGw2waXesRrQDug5Mkirzs66WoijkScaEFAbW2a7jjvgRIrvqtk-8QIeRVKUhw"
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
    get_for_refresh()