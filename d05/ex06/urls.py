from django.urls import path
from .views.init import Init
from .views.populate import Populate
from .views.display import Display
from .views.update import Update

urlpatterns = [
    path('init/', Init.as_view(), name='init'),
    path('populate/', Populate.as_view(), name='populate'),
    path('display/', Display.as_view(), name='display'),  # Asegúrate de que esta ruta muestra las películas
    path('update/', Update.as_view(), name='update'),    # Asegúrate de que esta ruta maneja la actualización
]
