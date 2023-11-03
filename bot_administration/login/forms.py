from django import forms



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username", "type": "text",
                                                             "placeholder": "Введите имя пользователя или почту"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "password", "type": "password", "placeholder": "Введите пароль"}),
    )

class ApplicationLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "username", "type": "text",
                                                             "placeholder": "Введите имя пользователя или почту"}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"autocomplete": "password", "type": "password", "placeholder": "Введите пароль"}),
    )
    application_id = forms.CharField(widget=forms.TextInput(attrs={"autocomplete": "application_id", "type": "text",
                                                             "placeholder": "Введите id приложения, который вам сообщил админ"}))
