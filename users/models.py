import uuid

from django.contrib.auth.models import User, AbstractUser
from django.db import models


class OneTimeCode(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Новый пользователь",
        on_delete=models.CASCADE,
    )
    code = models.CharField(
        max_length=64,
        verbose_name="Одноразовый код",
    )

    def __str__(self):
        return f"'{self.code}' для '{self.user}'"

    @staticmethod
    def create_for_user(user):
        otp_code = OneTimeCode()
        otp_code.user = user
        # Я не знаю каких-то хитрых методов, попробую UUID
        otp_code.code = uuid.uuid4().hex
        otp_code.save()

        return otp_code
