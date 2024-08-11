from django.shortcuts import render
from .forms import SearchForm
from .models import Movies, People, Planets

def search(request):
    results = None
    form = SearchForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        min_date = form.cleaned_data.get('min_release_date')
        max_date = form.cleaned_data.get('max_release_date')
        min_diameter = form.cleaned_data.get('min_diameter')
        gender = form.cleaned_data.get('gender')

        query = People.objects.all()
        if gender:
            query = query.filter(gender=gender)
        if min_date and max_date:
            query = query.filter(movies__release_date__range=(min_date, max_date))
        if min_diameter:
            query = query.filter(homeworld__diameter__gte=min_diameter)

        results = query.values('name', 'gender', 'movies__title', 'homeworld__name', 'homeworld__diameter')
    
    return render(request, 'ex10/search.html', {'form': form, 'results': results})

