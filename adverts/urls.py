from django.urls import path
from . import views

urlpatterns = [
    path("new", views.create_advert, name="create_advert"),
    path("<int:pk>/edit", views.edit_advert, name="edit_advert"),
    path("<int:pk>", views.view_advert, name="view_advert"),
    path("<int:advert_pk>/reply", views.create_reply, name="create_reply"),
    path("", views.index, name="index"),
]
