from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from adverts.forms import NewAdvertForm
from adverts.models import Advert, AdvertType


def index(request):
    all_adverts = Advert.objects.all().order_by("-created_at")
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
