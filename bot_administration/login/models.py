from django.db import models

# Create your models here.
class BotUser(models.Model):
    domain = models.CharField(max_length=50)
    tg_id = models.CharField(max_length=50, unique=True)
    choices = [("Application", "Application"), ("Bearer", "Bearer")]
    auth_type = models.CharField(max_length=12, choices=choices)
    application_token = models.CharField(null=True, max_length=50)
    refresh_token = models.CharField(null=True, max_length=50)

    def __str__(self):
        return f"{self.domain} {self.tg_id} {self.auth_type}"