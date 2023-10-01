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
        "client_id": "fd08333e8ef6751bf03c",
        "client_secret":"b45652af2b0ae6c750da8d3e8a177a93814d8a2e", 
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
    github_login("e9b9a66c973f06507c54")
    #get_github_access_token("1ce98809d2dc76f50ddc")