from django.urls import path
from .views import classic_login
urlpatterns = [
    path('standard', classic_login),
]
