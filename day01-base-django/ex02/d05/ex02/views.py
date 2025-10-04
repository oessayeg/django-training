from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
import logging
from d05 import settings

logger = logging.getLogger("ex02")


def form_view(request):
    if request.method == "POST":
        form = forms.TextForm(request.POST)
        if form.is_valid():
            logger.info(f"{form.cleaned_data['text_field']}")
            return redirect('form_view')
        else:
            return HttpResponse("Form is invalid")

    form = forms.TextForm()
    with open(f"{settings.LOGS_DIR}/app.log", "r") as logs:
        form_history = logs.read()
    return render(request, "form.html", {
        "form": form, 
        "form_history": form_history
    })
