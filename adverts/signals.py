from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Advert


@receiver(post_save, sender=Advert)
def notify_new_advert(sender, instance, **kwargs):
    send_mail(
        "Вы создали новое объявление",
        render_to_string(
            template_name="adverts/new_advert.txt",
            context={
                "username": instance.author.username,
                "advert": instance,
            },
        ),
        "noreply@adboard.fake",
        [instance.author.email],
        fail_silently=False,
    )
