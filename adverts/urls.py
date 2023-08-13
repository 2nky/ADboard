from django.urls import path
from . import views

urlpatterns = [
    path("new", views.create_advert, name="create_advert"),
    path("replies", views.list_replies, name="list_replies"),
    path("replies/<int:reply_pk>", views.view_reply, name="view_reply"),
    path("replies/<int:reply_pk>/accept", views.accept_reply, name="accept_reply"),
    path("replies/<int:reply_pk>/delete", views.delete_reply, name="delete_reply"),
    path("<int:pk>/edit", views.edit_advert, name="edit_advert"),
    path("<int:pk>", views.view_advert, name="view_advert"),
    path("<int:advert_pk>/reply", views.create_reply, name="create_reply"),
    path("", views.index, name="index"),
]
