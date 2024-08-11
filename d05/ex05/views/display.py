from django.views import View
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Movies


class Display(View):
    def get(self, request):
        movies = Movies.objects.all()
        if not movies:
            return HttpResponse("No data available")

        context = {'movies': movies}
        return render(request, 'ex05/display.html', context)