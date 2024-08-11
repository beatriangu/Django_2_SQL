
from django.conf import settings
from django.http import HttpResponse
from django.views import View
import psycopg2
import os

class Populate(View):
    table_planets = "ex08_planets"
    table_people = "ex08_people"

    def get(self, request):
        try:
            conn = psycopg2.connect(
                dbname=settings.DATABASES['default']['NAME'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                host=settings.DATABASES['default']['HOST'],
                port=settings.DATABASES['default']['PORT'],
            )
            with conn:
                with conn.cursor() as curs:
                    # table cleaning before insertion
                    curs.execute(f"TRUNCATE TABLE {self.table_planets} CASCADE;")
                    curs.execute(f"TRUNCATE TABLE {self.table_people} CASCADE;")

                    # Populate ex08_planets
                    planets_path = os.path.join(settings.BASE_DIR, 'data', 'planets.csv')
                    with open(planets_path, 'r', encoding='utf-8') as f:
                        curs.copy_expert(
                            f"COPY {self.table_planets} (name, climate, diameter, orbital_period, population, rotation_period, surface_water, terrain) FROM STDIN WITH (FORMAT CSV, DELIMITER '\t', NULL 'NULL')",
                            f
                        )

                    # Populate ex08_people
                    people_path = os.path.join(settings.BASE_DIR, 'data', 'people.csv')
                    with open(people_path, 'r', encoding='utf-8') as f:
                        curs.copy_expert(
                            f"COPY {self.table_people} (name, birth_year, gender, eye_color, hair_color, height, mass, homeworld) FROM STDIN WITH (FORMAT CSV, DELIMITER '\t', NULL 'NULL')",
                            f
                        )
            return HttpResponse("Ok data inserted into both tables!")
        except Exception as e:
            return HttpResponse(f"Error populating tables: {e}")