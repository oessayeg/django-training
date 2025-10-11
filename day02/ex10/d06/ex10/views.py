from django.http import HttpResponse
from django.shortcuts import render
from . import models
from .forms import MovieFilterForm


def display(request):
    try:
        people = models.People.objects.select_related('homeworld').filter(
            homeworld__climate__icontains='windy'
        ).values("name", "homeworld__name", "homeworld__climate").order_by(
            "name"
        ).all()
        if len(people) == 0:
            message = (
                "No data available, please use the following command line "
                "before use: python3 manage.py loaddata ex09_initial_data.json"
            )
            return HttpResponse(message)
        return render(request, "table.html", {"people": people})
    except Exception as e:
        return HttpResponse(f"No data available: {e}")


def ex10(request):
    if request.method == "POST":
        form = MovieFilterForm(request.POST)
        if form.is_valid():
            min_release_date = form.cleaned_data["min_release_date"]
            max_release_date = form.cleaned_data["max_release_date"]
            planet_diameter = form.cleaned_data["planet_diameter"]
            gender = form.cleaned_data["gender"]
            movie_data = models.Movies.objects.filter(
                release_date__gte=min_release_date,
                release_date__lte=max_release_date,
                characters__homeworld__diameter__gte=planet_diameter,
                characters__gender=gender
            ).values(
                "title",
                "characters__name",
                "characters__gender",
                "characters__homeworld__name",
                "characters__homeworld__diameter"
            ).all()

            if len(movie_data) == 0:
                return HttpResponse("Nothing corresponding to your research")
            return render(request, "display.html", {"movie_data": movie_data})
    else:
        form = MovieFilterForm()
        return render(request, "form.html", {"form": form})
