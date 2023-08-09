from django.urls import path
from . import views

urlpatterns = [
    path("new", views.create_advert, name="create_advert"),
    path("<int:pk>", views.view_advert, name="view_advert"),
    path("", views.index, name="index"),
]
