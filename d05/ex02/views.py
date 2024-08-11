from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
import psycopg2

TABLE_NAME = "ex02_movies"

def get_connection():
    return psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST'],
        port=settings.DATABASES['default']['PORT'],
    )

def init(request: HttpRequest):
    conn = None
    try:
        conn = get_connection()
        DROP_TABLE = f"DROP TABLE IF EXISTS {TABLE_NAME};"
        CREATE_TABLE = f"""
            CREATE TABLE {TABLE_NAME} (
                title VARCHAR(64) UNIQUE NOT NULL,
                episode_nb INT PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
        """
        with conn.cursor() as curs:
            curs.execute(DROP_TABLE)
            curs.execute(CREATE_TABLE)
        conn.commit()
        return HttpResponse("OK like ex00 specifications!")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

def populate(request: HttpRequest):
    conn = None
    try:
        conn = get_connection()

        movies = [
            (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
            (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
            (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
            (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
            (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
            (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
            (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11")
        ]

        INSERT_DATA = f"""
            INSERT INTO {TABLE_NAME} (
                episode_nb, title, director, producer, release_date
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (episode_nb) DO NOTHING;
            """

        result = []

        with conn.cursor() as curs:
            for movie in movies:
                try:
                    curs.execute(INSERT_DATA, movie)
                    conn.commit()
                    result.append(f"OK for {movie[1]}")
                except psycopg2.DatabaseError as e:
                    conn.rollback()
                    result.append(f"Error for {movie[1]}: {str(e)}")
        return HttpResponse("<br/>".join(result))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()

def display(request: HttpRequest):
    conn = None
    try:
        conn = get_connection()

        SELECT_TABLE = f"SELECT * FROM {TABLE_NAME};"
        with conn.cursor() as curs:
            curs.execute(SELECT_TABLE)
            movies = curs.fetchall()
        return render(request, 'ex02/display.html', {"movies": movies})
    except Exception as e:
        return HttpResponse(f"No data available. Error: {str(e)}")
    finally:
        if conn:
            conn.close()
