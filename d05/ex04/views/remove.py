# ex04/views/remove.py

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from ..forms import RemoveForm
import psycopg2

TABLE_NAME = "ex04_movies"

class Remove(View):
    template = "ex04/remove.html"

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
        Handles GET requests to display the removal form with the list of movie titles.
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as curs:
                # Fetch titles from the database
                curs.execute(f"SELECT title FROM {TABLE_NAME};")
                movies = curs.fetchall()
            
            # Prepare choices for the form
            choices = [(movie[0], movie[0]) for movie in movies]
            form = RemoveForm(choices=choices)
            
            context = {'form': form}
            return render(request, self.template, context)
        except Exception as e:
            print(f"Error during GET request: {e}")
            return HttpResponse("No data available")
        finally:
            if conn:
                conn.close()

    def post(self, request):
        """
        Handles POST requests to delete a movie and redisplay the form.
        """
        try:
            conn = self.get_connection()
            with conn.cursor() as curs:
                # Fetch titles from the database
                curs.execute(f"SELECT title FROM {TABLE_NAME};")
                movies = curs.fetchall()
            
            # Prepare choices for the form with POST data
            choices = [(movie[0], movie[0]) for movie in movies]
            form = RemoveForm(choices=choices, data=request.POST)
            
            if form.is_valid():
                title = form.cleaned_data['title']
                try:
                    with conn.cursor() as curs:
                        # Delete the selected movie
                        curs.execute(f"DELETE FROM {TABLE_NAME} WHERE title = %s", [title])
                    conn.commit()
                except Exception as e:
                    print(f"Error during DELETE operation: {e}")
            else:
                print(f"Form errors: {form.errors}")
        except Exception as e:
            print(f"Error during POST request: {e}")
        finally:
            if conn:
                conn.close()
        
        return redirect(request.path)

