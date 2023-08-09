from django.shortcuts import render

from adverts.models import Advert


def index(request):
    all_adverts = Advert.objects.all().order_by("-created_at")

    return render(request, "adverts/list.html", context={"adverts": all_adverts})
