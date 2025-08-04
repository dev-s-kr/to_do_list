from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth import login as django_login

def sign_up(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.LOGIN_URL)

    context = {
        "form": form
    }

    return render(request, "registeration/signup.html", context)

def login(request):
    form = AuthenticationForm(request, request.POST or None)

    if form.is_valid():
        django_login(request, form.get_user())
        next = request.GET.get("next")
        if next:
            return redirect(next)
        from django.urls import reverse
        return redirect(reverse("ToDoList:list"))

    context = {
        "form": form
    }

    return render(request, "registeration/login.html", context)
