# ex04/urls.py

from django.urls import path
from .views.init import Init
from .views.populate import Populate
from .views.display import Display
from .views.remove import Remove

urlpatterns = [
    path('init/', Init.as_view(), name='ex04-init'),
    path('populate/', Populate.as_view(), name='ex04-populate'),
    path('display/', Display.as_view(), name='ex04-display'),
    path('remove/', Remove.as_view(), name='ex04-remove'),
]
