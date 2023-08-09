from django.db import models
from django.db.models import Model


class AdvertType(Model):
    name = models.CharField(
        max_length=64,
        verbose_name="Название категории",
        blank=False,
    )

    class Meta:
        verbose_name = "Категория объявления"
        verbose_name_plural = "Категории объявлений"


class Advert(Model):
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

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
