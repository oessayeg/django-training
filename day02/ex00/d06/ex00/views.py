from django.http import HttpResponse
import psycopg2
from d06 import settings

HOST = settings.DATABASES["default"]["HOST"]
DATABASE = settings.DATABASES["default"]["NAME"]
PORT = settings.DATABASES["default"]["PORT"]
USER = settings.DATABASES["default"]["USER"]
PASSWORD = settings.DATABASES["default"]["PASSWORD"]


def init(request):
    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
        user=USER,
        password=PASSWORD,
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
