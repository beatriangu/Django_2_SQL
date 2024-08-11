from django.urls import path
from .views import Populate, Display, Update

app_name = 'ex07'

urlpatterns = [
    path('populate/', Populate.as_view(), name='populate'),
    path('display/', Display.as_view(), name='display'),
    path('update/', Update.as_view(), name='update'),
]
