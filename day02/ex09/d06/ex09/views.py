from django.http import HttpResponse
from django.shortcuts import render
from . import models


def display(request):
    try:
        people = models.People.objects.select_related('homeworld').filter(
            homeworld__climate__icontains='windy'
        ).values("name", "homeworld__name", "homeworld__climate").order_by(
            "name"
        ).all()
        if len(people) == 0:
            return HttpResponse("No data available, please use the following command line before use: python3 manage.py loaddata ex09_initial_data.json")
        return render(request, "table.html", {"people": people})
    except Exception as e:
        return HttpResponse(f"No data available: {e}")
