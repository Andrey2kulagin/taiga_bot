from django.shortcuts import render
from .forms import LoginForm
from .services.classic_login_service import login
# Create your views here.
def classic_login(request):# Получаем значения параметров из запроса
    context = {}
    # здесь будет приниматься 2 гет-параметра и обрабатываться пост-запрос на авторизацию по логину и паролю
    domain = request.GET.get('domain')
    tg_id = request.GET.get('tg_id')
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        if login(domain, username, password, tg_id) == 200:
            return render(request, 'login/success_login.html')
    form = LoginForm()
    context["form"] = form

    # Возвращаем HTML-страницу с результатами
    return render(request, 'login/standard_login.html', context)

def application_login(request):
    # здесь будет тоже самое, только сохраняться будет иначе
    pass