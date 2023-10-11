from django.shortcuts import render
from .forms import LoginForm, ApplicationLoginForm
from .services.classic_login_service import login
from .services.all_service import domain_validate_and_normalize

from .services.application_login_service import get_application_ver_token, application_login_handler

def classic_login(request):
    context = {}
    # здесь принимаеться 2 гет-параметра и обрабатываться пост-запрос на авторизацию по логину и паролю
    if request.GET.get("domain") is None or request.GET.get("tg_id") is None:
        return render(request, 'login/message_template.html', {"message": "Ошибка в ссылке, не переданы обязательные параметры. Проверьте правильность ссылки или обратитесь к администратору бота"})
    status, domain = domain_validate_and_normalize(request.GET.get('domain'))
    if status == False:
        return render(request, 'login/message_template.html', {"message": domain})
    tg_id = request.GET.get('tg_id')
    
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        if login(domain, username, password, tg_id) == 200:
            return render(request, 'login/message_template.html', {"message": "Вы успешно вошли! Можете закрыть страницу и возвратиться в бот"})
        context["error_message"] = "Неправильный логин или пароль, попробуйте ещё раз"
        form = LoginForm(post_data)
        context["form"] = form
        return render(request, 'login/standard_login.html', context)
    form = LoginForm()
    context["form"] = form
    return render(request, 'login/standard_login.html', context)



def application_login(request):
    # здесь принимается 2 гет-параметра и обрабатываться пост-запрос на авторизацию по логину и паролю и коду приложения
    context = {}
    if request.GET.get("domain") is None or request.GET.get("tg_id") is None:
        return render(request, 'login/message_template.html', {"message": "Ошибка в ссылке, не переданы обязательные параметры. Проверьте правильность ссылки или обратитесь к администратору бота"})
    status, domain = domain_validate_and_normalize(request.GET.get('domain'))
    if status == False:
        return render(request, 'login/message_template.html', {"message": domain})
    tg_id = request.GET.get('tg_id')
    if request.method == "POST":
        post_data = request.POST
        username = post_data.get("username")
        password = post_data.get("password")
        application_id = post_data.get("application_id")
        status, msg = application_login_handler(username, password, application_id, domain, tg_id)
        if status == 200:
            return render(request, 'login/message_template.html', {"message": "Вы успешно вошли! Можете закрыть страницу и возвратиться в бот"})
        else:
            return render(request, 'login/message_template.html', {"message": msg})
    form = ApplicationLoginForm()
    context["form"] = form
    return render(request, 'login/application_login.html', context)