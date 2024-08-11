# ex04/views/populate.py

from django.conf import settings
from django.http import HttpResponse
from django.views import View
import psycopg2

# Define el nombre de la tabla a usar en la base de datos
TABLE_NAME = "ex04_movies"

class Populate(View):
    def get_connection(self):
        """
        Establishes a connection to the PostgreSQL database using credentials from settings.
        """
        return psycopg2.connect(
            dbname=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )

    def get(self, request):
        """
        Handles GET requests to insert or update movie data in the ex04_movies table.
        """
        conn = None
        try:
            # Establish a connection to the database
            conn = self.get_connection()

            # Data to be inserted into the table
            movies = [
                (1, "The Phantom Menace", "George Lucas", "Rick McCallum", "1999-05-19"),
                (2, "Attack of the Clones", "George Lucas", "Rick McCallum", "2002-05-16"),
                (3, "Revenge of the Sith", "George Lucas", "Rick McCallum", "2005-05-19"),
                (4, "A New Hope", "George Lucas", "Gary Kurtz, Rick McCallum", "1977-05-25"),
                (5, "The Empire Strikes Back", "Irvin Kershner", "Gary Kurtz, Rick McCallum", "1980-05-17"),
                (6, "Return of the Jedi", "Richard Marquand", "Howard G. Kazanjian, George Lucas, Rick McCallum", "1983-05-25"),
                (7, "The Force Awakens", "J. J. Abrams", "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "2015-12-11")
            ]

            # SQL statement for inserting or updating data
            INSERT_DATA = f"""
            INSERT INTO {TABLE_NAME} (
                episode_nb, title, director, producer, release_date
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (episode_nb) 
            DO UPDATE SET 
                title = EXCLUDED.title,
                director = EXCLUDED.director,
                producer = EXCLUDED.producer,
                release_date = EXCLUDED.release_date;
            """

            result = []

            # Execute SQL commands
            with conn.cursor() as curs:
                for movie in movies:
                    try:
                        curs.execute(INSERT_DATA, movie)
                        conn.commit()
                        result.append(f"OK for {movie[1]}")
                    except psycopg2.DatabaseError as e:
                        conn.rollback()
                        result.append(f"Error for {movie[1]}: {str(e)}")

            # Return the result as an HTTP response
            return HttpResponse("<br/>".join(result))
        except Exception as e:
            # Handle any unexpected errors
            return HttpResponse(f"Error: {str(e)}")
        finally:
            # Ensure the connection is closed
            if conn:
                conn.close()

   
