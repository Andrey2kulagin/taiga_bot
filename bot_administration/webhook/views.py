from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class WebhookReceiver(APIView):
    def post(self, request, format=None):
        data = request.data  # Получаем данные из POST-запроса
        user_id = data['by']['id']
        return [user_id, data]
