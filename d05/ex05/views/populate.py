from django import db
from django.views import View
from django.http import HttpResponse
from ..models import Movies

class Populate(View):
    def get(self, request):
        movies = [
            {"episode_nb": 1, "title": "The Phantom Menace", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "1999-05-19"},
            {"episode_nb": 2, "title": "Attack of the Clones", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "2002-05-16"},
            {"episode_nb": 3, "title": "Revenge of the Sith", "director": "George Lucas", "producer": "Rick McCallum", "release_date": "2005-05-19"},
            {"episode_nb": 4, "title": "A New Hope", "director": "George Lucas", "producer": "Gary Kurtz, Rick McCallum", "release_date": "1977-05-25"},
            {"episode_nb": 5, "title": "The Empire Strikes Back", "director": "Irvin Kershner", "producer": "Gary Kurtz, Rick McCallum", "release_date": "1980-05-17"},
            {"episode_nb": 6, "title": "Return of the Jedi", "director": "Richard Marquand", "producer": "Howard G. Kazanjian, George Lucas, Rick McCallum", "release_date": "1983-05-25"},
            {"episode_nb": 7, "title": "The Force Awakens", "director": "J. J. Abrams", "producer": "Kathleen Kennedy, J. J. Abrams, Bryan Burk", "release_date": "2015-12-11"},
        ]

        result = []
        for movie_data in movies:
            movie, created = Movies.objects.update_or_create(
                episode_nb=movie_data['episode_nb'],
                defaults=movie_data
            )
            if created:
                result.append(f"OK for {movie.title}")
            else:
                result.append(f"OK for {movie.title}")

        if not result:
            return HttpResponse("No data available")

        return HttpResponse("<br/>".join(result))
