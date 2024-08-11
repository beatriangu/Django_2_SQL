# views.py

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import View
import psycopg2
from ..forms import UpdateForm

class Update(View):
    TABLE_NAME = "ex06_movies"
    template = 'ex06/update.html'

    def get(self, request):
        SELECT_TABLE = f"SELECT title FROM {self.TABLE_NAME};"
        
        try:
            with psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
            ) as conn:
                with conn.cursor() as curs:
                    curs.execute(SELECT_TABLE)
                    movies = curs.fetchall()
            
            if not movies:
                return HttpResponse("No data available")
            
            form = UpdateForm(choices=[(movie[0], movie[0]) for movie in movies])
            context = {'form': form}
            return render(request, self.template, context)
        
        except Exception as e:
            print(f"Error in GET request: {e}")
            return HttpResponse("No data available")

    def post(self, request):
        SELECT_TABLE = f"SELECT title FROM {self.TABLE_NAME};"
        
        try:
            with psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
            ) as conn:
                with conn.cursor() as curs:
                    curs.execute(SELECT_TABLE)
                    movies = curs.fetchall()
            
            choices = [(movie[0], movie[0]) for movie in movies]
        
        except Exception as e:
            print(f"Error retrieving choices: {e}")
            return HttpResponse("No data available")

        form = UpdateForm(choices, request.POST)
        
        if form.is_valid():
            UPDATE_SQL = f"UPDATE {self.TABLE_NAME} SET opening_crawl = %s WHERE title = %s"
            
            try:
                with psycopg2.connect(
                    dbname=settings.DATABASES['default']['NAME'],
                    user=settings.DATABASES['default']['USER'],
                    password=settings.DATABASES['default']['PASSWORD'],
                    host=settings.DATABASES['default']['HOST'],
                    port=settings.DATABASES['default']['PORT'],
                ) as conn:
                    with conn.cursor() as curs:
                        curs.execute(
                            UPDATE_SQL,
                            [form.cleaned_data['opening_crawl'], form.cleaned_data['title']]
                        )
                        conn.commit()
            
            except Exception as e:
                print(f"Error updating data: {e}")
                return HttpResponse("No data available")
            
            return redirect('display')
        
        else:
            print("Form errors:", form.errors)  # Añadido para la depuración
            return render(request, self.template, {'form': form})
