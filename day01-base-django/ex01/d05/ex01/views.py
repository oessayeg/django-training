from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


# Create your views here.
def django(request: HttpRequest):
    html_page_title = "Ex01: Django, framework web."
    django_description_and_history = (
        "Django is a free and open-source, Python-based web framework that runs on a web server. It follows the model–template–views (MTV) "
        "architectural pattern. It is maintained by the Django Software Foundation (DSF), an independent organization established in the US "
        "as a 501(c)(3) non-profit. Django's primary goal is to ease the creation of complex, database-driven websites. The framework emphasizes "
        "reusability and 'pluggability' of components, less code, low coupling, rapid development, and the principle of don't repeat yourself."
        " Python is used throughout, even for settings, files, and data models. Django also provides an optional administrative create, "
        "read, update and delete interface that is generated dynamically through introspection and configured via admin models."
        "Django was created in the autumn of 2003, when the web programmers at the Lawrence Journal-World newspaper, "
        "Adrian Holovaty and Simon Willison, began using Python to build applications. Jacob Kaplan-Moss was hired early in "
        "Django's development shortly before Willison's internship ended. It was released publicly under a BSD license "
        "in July 2005. The framework was named after guitarist Django Reinhardt. Holovaty is a romani jazz guitar player inspired in part by Reinhardt's music."
    )
    return render(request, 'base.html', {
        "title": html_page_title,
        "content": django_description_and_history
    })


def display(request: HttpRequest):
    return HttpResponse("Hello from display")


def templates(request: HttpRequest):
    return HttpResponse("Hello from templates")
