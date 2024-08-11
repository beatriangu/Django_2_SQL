
from django.contrib import admin
from .models import Planets, People

@admin.register(Planets)
class PlanetsAdmin(admin.ModelAdmin):
    list_display = ('name', 'climate', 'diameter', 'orbital_period', 'population', 'rotation_period', 'surface_water', 'terrain', 'created', 'updated')

@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_year', 'gender', 'eye_color', 'hair_color', 'height', 'mass', 'homeworld', 'created', 'updated')
