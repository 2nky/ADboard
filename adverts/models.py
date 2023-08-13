from django.contrib.auth.models import User
from django.db import models
from django.db.models import Model


class AdvertType(Model):
    name = models.CharField(
        max_length=64,
        verbose_name="Название категории",
        blank=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория объявления"
        verbose_name_plural = "Категории объявлений"


class Advert(Model):
    author = models.ForeignKey(
        User,
        verbose_name="Автор объявления",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )
    category = models.ForeignKey(
        AdvertType,
        verbose_name="Категория",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    header = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        blank=False,
        null=True,
    )
    text = models.TextField(
        verbose_name="Текст объявления",
        null=False,
        blank=False,
    )

    def __str__(self):
        return f"{self.author.username}: {self.header} [{self.category.name}]"

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Reply(Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор отклика",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    advert = models.ForeignKey(
        Advert,
        verbose_name="На объявление",
        null=False,
        blank=False,
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name="Текст отклика",
        null=False,
        blank=False,
    )
    accepted = models.BooleanField(
        verbose_name="Принято",
        default=False,
    )

    def __str__(self):
        return f"{self.author.username} на '{self.advert.header}' (символов: {len(self.text)})"

    class Meta:
        verbose_name = "Отклик на объявление"
        verbose_name_plural = "Отклики на объявления"
