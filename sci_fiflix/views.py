from django.shortcuts import render
from .models import Movie

def home(request):
    trending_movies = Movie.objects.filter(is_trending=True)
    new_releases = Movie.objects.order_by('-release_date')[:6]

    context = {
        'trending_movies': trending_movies,
        'new_releases': new_releases,
    }
    return render(request, 'home.html', context)
