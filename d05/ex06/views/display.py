# views.py

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import psycopg2

class Display(View):
    template = 'ex06/display.html'
    TABLE_NAME = "ex06_movies"

    def get(self, request):
        SELECT_TABLE = f"SELECT * FROM {self.TABLE_NAME};"
        
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
            
            context = {'movies': movies}
            return render(request, self.template, context)
        
        except Exception as e:
            print(f"Error in GET request: {e}")
            return HttpResponse("No data available")
