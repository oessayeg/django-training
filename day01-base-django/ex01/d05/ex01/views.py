from django.shortcuts import render
from django.http import HttpRequest


def django(request: HttpRequest):
    return render(request, 'django.html')


def display(request: HttpRequest):
    return render(request, 'display.html')


def templates(request: HttpRequest):
    return render(request, 'templates.html')
