# ex04/views.py

from django.conf import settings
from django.http import HttpResponse
from django.views import View
import psycopg2

TABLE_NAME = "ex04_movies"

class Init(View):
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
        Handles GET requests to create the table.
        """
        conn = None
        try:
            conn = self.get_connection()
            create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                title VARCHAR(64) NOT NULL UNIQUE,
                episode_nb INT PRIMARY KEY,
                opening_crawl TEXT,
                director VARCHAR(32) NOT NULL,
                producer VARCHAR(128) NOT NULL,
                release_date DATE NOT NULL
            );
            """
            with conn.cursor() as curs:
                curs.execute(create_table_query)
            conn.commit()
            return HttpResponse("OK")
        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")
        finally:
            if conn:
                conn.close()

