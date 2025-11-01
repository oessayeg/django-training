from django.http import HttpResponse
from django.shortcuts import render
import psycopg2
from d06 import settings
from io import StringIO
import os

DB_SETTINGS = settings.DATABASES["default"]
HOST = DB_SETTINGS["HOST"]
DATABASE = DB_SETTINGS["NAME"]
PORT = DB_SETTINGS["PORT"]
USER = DB_SETTINGS["USER"]
PASSWORD = DB_SETTINGS["PASSWORD"]
BASE_DIR = settings.BASE_DIR


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
                    CREATE TABLE IF NOT EXISTS ex08_planets (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(64) UNIQUE NOT NULL,
                        climate VARCHAR,
                        diameter INTEGER,
                        orbital_period INTEGER,
                        population BIGINT,
                        rotation_period INTEGER,
                        surface_water REAL,
                        terrain VARCHAR(128)
                    );
                """)
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS ex08_people (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64) UNIQUE NOT NULL,
                    birth_year VARCHAR(32),
                    gender VARCHAR(32),
                    eye_color VARCHAR(32),
                    hair_color VARCHAR(32),
                    height INTEGER,
                    mass REAL,
                    homeworld VARCHAR(64),
                    FOREIGN KEY (homeworld) REFERENCES ex08_planets(name)
                );
                """)
                connection.commit()
                return HttpResponse("OK")
            except Exception as e:
                return HttpResponse(f"Error initializing database: {e}")


def populate_table_from_csv(cursor, filename, table_name, columns, sep="\t"):
    csv_path = os.path.join(BASE_DIR, filename)

    with open(csv_path, "r") as csv_file:
        csv_data = csv_file.read()

        csv_buffer = StringIO(csv_data)
        cursor.copy_from(csv_buffer, table_name, sep=sep, columns=columns, null="NULL")


def populate(request):
    http_response_message = []

    planets_columns = (
        "name",
        "climate",
        "diameter",
        "orbital_period",
        "population",
        "rotation_period",
        "surface_water",
        "terrain",
    )
    people_columns = (
        "name",
        "birth_year",
        "gender",
        "eye_color",
        "hair_color",
        "height",
        "mass",
        "homeworld",
    )

    table_data = [
        {
            "filename": "planets.csv",
            "table_name": "ex08_planets",
            "columns": planets_columns,
        },
        {
            "filename": "people.csv",
            "table_name": "ex08_people",
            "columns": people_columns,
        },
    ]

    with psycopg2.connect(
        host=HOST,
        database=DATABASE,
        port=PORT,
        user=USER,
        password=PASSWORD,
    ) as connection:
        with connection.cursor() as cursor:
            for table in table_data:
                try:
                    populate_table_from_csv(
                        cursor, table["filename"], table["table_name"], table["columns"]
                    )
                    http_response_message.append("OK")
                except Exception as e:
                    message = f"Error populating database: {e}"
                    http_response_message.append(message)
                    connection.rollback()

    if http_response_message:
        return HttpResponse("<br>".join(http_response_message))
    return HttpResponse("OK")


def display(request):
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
                    SELECT ex08_people.name, homeworld, climate FROM ex08_people
                    LEFT JOIN ex08_planets
                    ON ex08_people.homeworld = ex08_planets.name
                    WHERE ex08_planets.climate LIKE '%windy%'
                    ORDER BY ex08_people.name
                """)
                data_list = cursor.fetchall()

                if len(data_list) == 0:
                    return HttpResponse("No data available")
                return render(request, "display.html", {"people": data_list})
            except Exception:
                return HttpResponse("No data available")
