from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm
from .models import User
from .models import User, BlockedIP
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger("auth_app")

MAX_FAILED_ATTEMPTS = 5
LOCK_TIME_DURATION = timedelta(minutes=5)
IP_BLOCK_DURATION = timedelta(minutes=10)


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(request, "auth_app/register.html", {"form": form})


def login_view(request):

    ip_address = request.META.get("REMOTE_ADDR")

    blocked_ip = BlockedIP.objects.filter(ip_address=ip_address).first()

    if blocked_ip and timezone.now() < blocked_ip.blocked_until:
        messages.error(request, "Too many attempts from this IP. Try again later.")
        return redirect("login")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)

            # Check if account is locked
            if user.is_locked:

                # Check if lock time has expired
                if user.lock_time and timezone.now() > user.lock_time + LOCK_TIME_DURATION:
                    user.is_locked = False
                    user.failed_login_attempts = 0
                    user.lock_time = None
                    user.save()

                else:
                    messages.error(request, "Account locked. Try again later.")
                    return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            user.failed_login_attempts = 0
            user.save()

            login(request, user)
            return redirect("dashboard")

        else:
            user = User.objects.get(username=username)
            user.failed_login_attempts += 1

            logger.warning(
                f"Failed login attempt | username={username} | ip={ip_address}"
            )

            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                user.is_locked = True
                user.lock_time = timezone.now()
                BlockedIP.objects.update_or_create(
                    ip_address=ip_address,
                    defaults={"blocked_until": timezone.now() + IP_BLOCK_DURATION}
                )

                logger.warning(
                    f"Account locked | username={username} | ip={ip_address}"
                )

            user.save()

            messages.error(request, "Invalid username or password")

    return render(request, "auth_app/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    return render(request, "auth_app/dashboard.html")