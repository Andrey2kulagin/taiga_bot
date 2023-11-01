from django.urls import path
from .views import WebhookReceiver

urlpatterns = [
    path('webhook/<str:user_tg_id>/<int:project_id>/', WebhookReceiver.as_view(), name='webhook'),
]