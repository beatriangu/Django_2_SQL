from django.shortcuts import render
from django.http import HttpResponse
from .models import Movies
from django.db import transaction

def populate(request):
    result = []
    movies_data = [
        {'episode_nb': 1, 'title': 'The Phantom Menace', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '1999-05-19'},
        {'episode_nb': 2, 'title': 'Attack of the Clones', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2002-05-16'},
        {'episode_nb': 3, 'title': 'Revenge of the Sith', 'director': 'George Lucas', 'producer': 'Rick McCallum', 'release_date': '2005-05-19'},
        {'episode_nb': 4, 'title': 'A New Hope', 'director': 'George Lucas', 'producer': 'Gary Kurtz, Rick McCallum', 'release_date': '1977-05-25'},
        {'episode_nb': 5, 'title': 'The Empire Strikes Back', 'director': 'Irvin Kershner', 'producer': 'Gary Kurtz, Rick McCallum', 'release_date': '1980-05-17'},
        {'episode_nb': 6, 'title': 'Return of the Jedi', 'director': 'Richard Marquand', 'producer': 'Howard G. Kazanjian, George Lucas, Rick McCallum', 'release_date': '1983-05-25'},
        {'episode_nb': 7, 'title': 'The Force Awakens', 'director': 'J. J. Abrams', 'producer': 'Kathleen Kennedy, J. J. Abrams, Bryan Burk', 'release_date': '2015-12-11'},
    ]

    for movie_data in movies_data:
        try:
            Movies.objects.update_or_create(
                episode_nb=movie_data['episode_nb'],
                defaults={
                    'title': movie_data['title'],
                    'director': movie_data['director'],
                    'producer': movie_data['producer'],
                    'release_date': movie_data['release_date'],
                }
            )
            result.append(f"OK for  {movie_data['title']}")
        except Exception as e:
            result.append(f"Error for {movie_data['episode_nb']} {str(e)}")

    return HttpResponse("<br/>".join(result))

def display(request):
    try:
        # Query the data
        movies = Movies.objects.all()

        # Render the data in HTML
        if movies:
            return render(request, 'ex03/display.html', {'movies': movies})
        else:
            return HttpResponse("No data available")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")


