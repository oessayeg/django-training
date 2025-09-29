from django.shortcuts import render
from django.http import HttpRequest


def markdown_info_view(request: HttpRequest):
    return render(request, "markdown_info.html")
