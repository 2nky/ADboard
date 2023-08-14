from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from adverts.forms import NewAdvertForm, ReplyForm
from adverts.models import Advert, AdvertType, Reply


def index(request):
    # Вместе с каждым объявлением в списке будем отдавать количество откликов
    all_adverts = Advert.objects.all().annotate(Count("reply")).order_by("-created_at")
    return render(
        request,
        "adverts/list.html",
        context={
            "adverts": all_adverts,
            "categories": AdvertType.objects.all(),
        },
    )


@login_required
def create_advert(request):
    if request.method == "POST":
        form = NewAdvertForm(request.POST)
        if form.is_valid():
            advert = Advert(
                author=request.user,
                category=form.cleaned_data["category"],
                header=form.cleaned_data["header"],
                text=form.cleaned_data["text"],
            )
            advert.save()

            messages.success(
                request, f"Вы успешно создали объявление: '{advert.header}'"
            )

            return redirect(reverse("index"))
        else:
            messages.error(request, "При обработке вашей форме произошли ошибки!")
    else:
        form = NewAdvertForm()

    return render(request, "adverts/new.html", {"form": form})


def view_advert(request, pk):
    try:
        advert = Advert.objects.get(pk=pk)
        return render(
            request,
            "adverts/view.html",
            {
                "advert": advert,
            },
        )
    except Advert.DoesNotExist:
        messages.error(request, "Запрашиваемое вами объявление не найдено")
        return redirect(reverse("index"))


@login_required
def edit_advert(request, pk):
    try:
        advert = Advert.objects.get(pk=pk)
        if request.method == "GET":
            form = NewAdvertForm(instance=advert)
        else:
            form = NewAdvertForm(request.POST)
            if form.is_valid():
                advert.header = form.cleaned_data["header"]
                advert.text = form.cleaned_data["text"]
                advert.category = form.cleaned_data["category"]
                advert.save()

                messages.success(request, "Изменения в объявления внесены!")

                return redirect(reverse("view_advert", kwargs={"pk": advert.pk}))

        return render(
            request,
            "adverts/edit.html",
            {
                "form": form,
                "advert": advert,
            },
        )
    except Advert.DoesNotExist:
        messages.error(request, "Запрашиваемое вами объявление не найдено")
        return redirect(reverse("index"))


@login_required
def create_reply(request, advert_pk):
    advert = get_object_or_404(Advert, pk=advert_pk)

    form = None
    if request.method == "POST":
        form = ReplyForm(request.POST)
        # commit=False нужен чтобы поля заполнить
        if form.is_valid():
            reply = form.save(commit=False)
            reply.author = request.user
            reply.advert = advert
            reply.save()

            messages.success(request, "Ваш отклик был сохранён!")
            return redirect(reverse("view_advert", kwargs={"pk": advert_pk}))
        else:
            messages.error(request, "При обработке вашего отклика были ошибки!")
    else:
        form = ReplyForm()

    return render(
        request,
        "replies/new.html",
        {
            "form": form,
            "advert": advert,
        },
    )


@login_required
def list_replies(request):
    replies = Reply.objects.filter(advert__author=request.user)

    return render(
        request,
        "replies/list.html",
        context={
            "replies": replies,
        },
    )


@login_required
def view_reply(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    return render(
        request,
        "replies/view.html",
        context={
            "advert": reply.advert,
            "reply": reply,
        },
    )


@login_required
def accept_reply(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.user == reply.advert.author:
        reply.accepted = True
        reply.save()

        messages.success(request, f"Вы приняли отклик от {reply.author.username}")
    else:
        messages.error(request, "Вы не автор объявления, вы не можете принять отклик!")

    return redirect(
        reverse(
            "view_reply",
            kwargs={
                "reply_pk": reply.pk,
            },
        )
    )


@login_required
def delete_reply(request, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)

    if request.user == reply.advert.author:
        reply.delete()

        messages.success(
            request,
            f"Вы успешно удалили отклик от {reply.author.username}",
        )
        return redirect(reverse("list_replies"))
    else:
        messages.error(
            request,
            f"Вы не можете удалить отклик не на своё объявления!",
        )
        return redirect(
            reverse(
                "view_reply",
                kwargs={
                    "reply_pk": reply.pk,
                },
            )
        )
