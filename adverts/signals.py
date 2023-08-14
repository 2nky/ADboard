from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Advert, Reply


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


@receiver(post_save, sender=Reply)
def notify_new_reply(sender, instance, **kwargs):
    send_mail(
        "Кто-то откликнулся на ваше объявление",
        render_to_string(
            template_name="replies/new_reply.txt",
            context={
                "reply": instance,
                "advert": instance.advert,
            },
        ),
        "noreply@adboard.fake",
        [instance.advert.author.email],
        fail_silently=False,
    )


@receiver(pre_save, sender=Reply)
def notify_reply_accepted(sender, instance, **kwargs):
    # Все новые отклики не приняты по умолчанию
    if instance.id is None:
        return

    previous = Reply.objects.get(pk=instance.pk)
    if instance.accepted and not previous.accepted:
        send_mail(
            "Ваш отклик был принят!",
            render_to_string(
                template_name="replies/reply_accepted.txt",
                context={
                    "reply": instance,
                    "advert": instance.advert,
                },
            ),
            "noreply@adboard.fake",
            [instance.author.email],
            fail_silently=False,
        )
