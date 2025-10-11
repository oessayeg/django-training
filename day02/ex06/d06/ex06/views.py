from django.http import HttpResponse
from django.shortcuts import render, redirect
import psycopg2
from d06 import settings

DB_SETTINGS = settings.DATABASES["default"]
HOST = DB_SETTINGS["HOST"]
DATABASE = DB_SETTINGS["NAME"]
PORT = DB_SETTINGS["PORT"]


def init(request):
    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
    ) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ex06_movies (
                        title VARCHAR(64) NOT NULL UNIQUE,
                        episode_nb INT PRIMARY KEY,
                        opening_crawl TEXT,
                        director VARCHAR(32) NOT NULL,
                        producer VARCHAR(128) NOT NULL,
                        release_date DATE NOT NULL,
                        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                cursor.execute("""
                    CREATE OR REPLACE FUNCTION update_changetimestamp_column()
                        RETURNS TRIGGER AS $$
                        BEGIN
                        NEW.updated = now();
                        NEW.created = OLD.created;
                        RETURN NEW;
                        END;
                        $$ language 'plpgsql';
                        CREATE TRIGGER update_films_changetimestamp BEFORE UPDATE
                        ON ex06_movies FOR EACH ROW EXECUTE PROCEDURE
                        update_changetimestamp_column();
                """)
                connection.commit()
                return HttpResponse("OK")
            except Exception as e:
                return HttpResponse(f"Error initializing database: {e}")


def populate(request):
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
    http_response_message = []

    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
    ) as connection:
        with connection.cursor() as cursor:
            for movie in movies_data:
                try:
                    cursor.execute(
                        """
                        INSERT INTO ex06_movies (
                            episode_nb,
                            title,
                            director,
                            producer,
                            release_date
                        ) VALUES (%s, %s, %s, %s, %s)
                    """,
                        movie,
                    )
                    connection.commit()
                    http_response_message.append("OK")
                except Exception as e:
                    http_response_message.append(f"Error inserting movie: {e}")
                    connection.rollback()

    return HttpResponse("<br>".join(http_response_message))


def display(request):
    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
    ) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("SELECT * FROM ex06_movies")
                data_list = cursor.fetchall()

                if len(data_list) == 0:
                    return HttpResponse("No data available")
                return render(request, "table.html", {"movies": data_list})
            except Exception:
                return HttpResponse("No data available")


def update(request):
    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
    ) as connection:
        with connection.cursor() as cursor:
            if request.method == "POST":
                title = request.POST.get("movie_title")
                opening_crawl = request.POST.get("opening_crawl")
                update_statement = """
                    UPDATE ex06_movies SET opening_crawl = %s WHERE title = %s
                """
                cursor.execute(update_statement, (opening_crawl, title))
                connection.commit()
                return redirect("update")
            try:
                cursor.execute("SELECT title FROM ex06_movies")
                data_list = cursor.fetchall()
                titles = [retrieved_data[0] for retrieved_data in data_list]

                if len(data_list) == 0:
                    return HttpResponse("No data available")
                return render(request, "dropdown.html", {"titles": titles})
            except Exception:
                return HttpResponse("No data available")
