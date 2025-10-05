from django.http import HttpResponse
import psycopg2


def init(request):
    with psycopg2.connect(
        host="localhost",
        database="my_db",
        port="5432",
    ) as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ex00_movies (
                        title VARCHAR(64) NOT NULL UNIQUE,
                        episode_nb INT PRIMARY KEY,
                        opening_crawl TEXT,
                        director VARCHAR(32) NOT NULL,
                        producer VARCHAR(128) NOT NULL,
                        release_date DATE NOT NULL
                    );
                """)
                connection.commit()
                return HttpResponse("OK")
            except Exception as e:
                return HttpResponse(f"Error initializing database: {e}")
