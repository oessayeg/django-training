from django.shortcuts import render, redirect
from django.db.models import Count, Exists, OuterRef
from . import forms
from . import models
from django.http import JsonResponse
    

def ex(request):
    username = request.session.get("username")
    anonymous_username = request.session.get("anonymous_username")
    reputation = 0
    current_user = None
    
    if username:
        current_user = models.User.objects.filter(username=username).first()
        if current_user:
            reputation = current_user.get_reputation()

    if username and request.method == "POST":
        tip_form = forms.TipForm(request.POST)
        if tip_form.is_valid():
            tip = tip_form.save(commit=False)
            tip.author_id = username
            tip.save()
            return redirect("/")
        else:
            return render(
                request, "welcome.html", {"username": username, "form": tip_form}
            )

    tip_form = forms.TipForm()
    all_tips = models.Tip.objects.annotate(
        total_upvotes=Count("upvoted_by"),
        total_downvotes=Count("downvoted_by"),
        is_upvoted=Exists(
            models.User.objects.filter(upvoted_tips=OuterRef("pk"), username=username)
        ),
        is_downvoted=Exists(
            models.User.objects.filter(downvoted_tips=OuterRef("pk"), username=username)
        ),
    ).select_related('author').all()

    tips_with_reputation = []
    for tip in all_tips:
        tip.author_reputation = tip.author.get_reputation()
        tips_with_reputation.append(tip)

    return render(
        request,
        "welcome.html",
        {
            "username": username,
            "anonymous_username": anonymous_username,
            "form": tip_form,
            "all_tips": tips_with_reputation,
            "reputation": reputation,
            "has_right_to_delete_tips": current_user.has_right_to_delete_tips if current_user else False,
            "can_downvote_tips": current_user.can_downvote_tips if current_user else False,
        },
    )


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
            new_user = models.User(username=registration_form.cleaned_data["username"])
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


def tip_action(request, tip_id):
    username = request.session.get("username")

    if not username:
        return redirect("/")

    if request.method == "POST":
        action = request.POST.get("action")
        tip = models.Tip.objects.filter(id=tip_id).first()
        user = models.User.objects.filter(username=username).first()

        if not tip or not user:
            return redirect("/")

        is_author = user.username == tip.author.username

        if action == "delete":
            if is_author or user.can_delete_tips():
                tip.delete()
        else:
            is_upvoted = tip.upvoted_by.filter(username=username).exists()
            is_downvoted = tip.downvoted_by.filter(username=username).exists()

            if action == "upvote":
                if is_upvoted:
                    tip.upvoted_by.remove(user)
                else:
                    if is_downvoted:
                        tip.downvoted_by.remove(user)
                    tip.upvoted_by.add(user)
            elif action == "downvote":
                if is_author or user.can_downvote():
                    if is_downvoted:
                        tip.downvoted_by.remove(user)
                    else:
                        if is_upvoted:
                            tip.upvoted_by.remove(user)
                        tip.downvoted_by.add(user)

    return redirect("/")


def get_anonymous_username(request):
    username = request.session.get("username")
    if username:
        return JsonResponse({"anonymous_username": None})
    
    anonymous_username = request.session.get("anonymous_username")
    return JsonResponse({"anonymous_username": anonymous_username})
