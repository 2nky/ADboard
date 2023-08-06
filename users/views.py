from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from users.forms import NewUserForm
from users.models import OneTimeCode


def register_user(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user.is_active = False
            new_user.save()

            new_code = OneTimeCode.create_for_user(new_user)

            # TODO: Выслать письмо пользователю
            send_mail(
                "Подтверждение учетной записи",
                render_to_string(
                    template_name="users/otp_code_letter.txt",
                    context={
                        "otp_code": new_code.code,
                    },
                ),
                "noreply@adboard.fake",
                [new_user.email],
                fail_silently=False,
            )

            return render(
                request,
                template_name="users/otp_code_sent.html",
                context={"email": new_user.email},
            )
        else:
            messages.error(
                request,
                "Не удалось завершить регистрацию. Проверьте данные!",
            )
    else:
        form = NewUserForm()

    return render(
        request=request,
        template_name="users/register.html",
        context={"form": form},
    )


def confirm_user(request, code):
    try:
        otp = OneTimeCode.objects.get(code=code)
        otp.user.is_active = True
        otp.user.save()

        login(request, otp.user)
        otp.delete()

        messages.success(request, "Вы успешно подтвердили свою учетную запись!")

        return redirect(reverse("index"))
    except OneTimeCode.DoesNotExist:
        pass


@login_required
def placeholder(request):
    return render(request, "users/placeholder.html")


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Вы успешно вошли в систему как '{username}'.")
                return redirect("index")
            else:
                messages.error(request, "Неправильное имя пользователя или пароль!")
        else:
            messages.error(request, "Неправильное имя пользователя или пароль!")
    else:
        form = AuthenticationForm()

    return render(
        request,
        template_name="users/login.html",
        context={
            "login_form": form,
        },
    )


def logout_user(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из системы.")
    return redirect("index")
