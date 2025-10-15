from django.shortcuts import render
from django.shortcuts import redirect
from . import forms
from . import models


def ex(request):
    username = request.session.get("username")
    if username and request.method == "POST":
        tip_form = forms.TipForm(request.POST)
        if tip_form.is_valid():
            tip = tip_form.save(commit=False)
            tip.author_id = username
            tip.save()
            return redirect("/")
        else:
            return render(request, "welcome.html", {"username": username, "form": tip_form})
    tip_form = forms.TipForm()
    all_tips = models.Tip.objects.all().order_by("-created")
    return render(request, "welcome.html", {"username": username, "form": tip_form, "all_tips": all_tips})


def login(request):
    username = request.session.get("username")
    if username:
        return redirect("/")
    if request.method == "POST":
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            try:
                user = models.User.objects.get(
                    username=login_form.cleaned_data["username"]
                )
                if user.check_password(login_form.cleaned_data["password"]):
                    request.session["username"] = login_form.cleaned_data["username"]
                    return redirect("/")
                else:
                    return render(
                        request,
                        "login.html",
                        {"error": "Invalid username or password", "form": login_form},
                    )
            except models.User.DoesNotExist:
                return render(
                    request,
                    "login.html",
                    {"error": "Invalid username or password", "form": login_form},
                )
        else:
            return render(request, "login.html", {"form": login_form})
    login_form = forms.LoginForm()
    return render(request, "login.html", {"form": login_form})


def registration(request):
    username = request.session.get("username")
    if username:
        return redirect("/")
    if request.method == "POST":
        registration_form = forms.RegistrationForm(request.POST)
        if registration_form.is_valid():
            already_exists = models.User.objects.filter(
                username=registration_form.cleaned_data["username"]
            ).exists()
            if already_exists:
                return render(
                    request,
                    "registration.html",
                    {"error": "Username already exists", "form": registration_form},
                )
            request.session["username"] = registration_form.cleaned_data["username"]
            new_user = models.User(
                username=registration_form.cleaned_data["username"]
            )
            new_user.set_password(registration_form.cleaned_data["password"])
            new_user.save()
            return redirect("/")
        else:
            return render(
                request,
                "registration.html",
                {
                    "form": registration_form,
                },
            )

    registration_form = forms.RegistrationForm()
    return render(request, "registration.html", {"form": registration_form})

def logout(request):
    request.session.clear()
    return redirect("/")
