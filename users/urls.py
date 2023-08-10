from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register_user"),
    path("confirm/<code>/", views.confirm_user, name="confirm_otp_code"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]
