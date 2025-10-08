from django.http import HttpResponse
from django.shortcuts import render
from . import models


def populate(request):
    http_response_message = []
    movies_data = (
        (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
        (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
        (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
        (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
        (
            5,
            "The Empire Strikes Back",
            "Irvin Kershner",
            "Gary Kurtz, Rick McCallum",
            "1980-05-17",
        ),
        (
            6,
            "Return of the Jedi",
            "Richard Marquand",
            "Howard G. Kazanjian, George Lucas, Rick McCallum",
            "1983-05-25",
        ),
        (
            7,
            "The Force Awakens",
            "J. J. Abrams",
            "Kathleen Kennedy, J. J. Abrams, Bryan Burk",
            "2015-12-11",
        ),
    )
    for movie in movies_data:
        try:
            if models.Movies.objects.filter(episode_nb=movie[0]).exists():
                http_response_message.append(
                    f"Movie with episode {movie[0]} already exists"
                )
            else:
                row = models.Movies(
                    episode_nb=movie[0],
                    title=movie[1],
                    director=movie[2],
                    producer=movie[3],
                    release_date=movie[4],
                )
                row.save()
                http_response_message.append("OK")
        except Exception as e:
            http_response_message.append(f"Error: {e}")
    return HttpResponse("<br>".join(http_response_message))


def display(request):
    try:
        movies = models.Movies.objects.all()
        if len(movies) == 0:
            return HttpResponse("No data available")
        return render(request, "table.html", {"movies": movies})
    except Exception:
        return HttpResponse("No data available")


def remove(request):
    if request.method == "POST":
        title = request.POST.get("movie_title")
        models.Movies.objects.filter(title=title).delete()

    try:
        titles_list = models.Movies.objects.values_list("title", flat=True)
        if len(titles_list) == 0:
            return HttpResponse("No data available")
        return render(request, "dropdown.html", {"titles": titles_list})
    except Exception:
        return HttpResponse("No data available")
