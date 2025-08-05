from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect

from .forms import SignUpForm


def logout_view(request):
    logout(request)
    return redirect('index')


def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save()
        perm = Permission.objects.get(codename="creator")
        user.refresh_from_db()  # Carrega a instância novamente
        user.author.bio = form.cleaned_data.get(
            "bio"
        )  # Atribui os outros dados ao user
        user.user_permissions.add(perm)  # Adiciona permissão de creator
        user.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("index")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})
