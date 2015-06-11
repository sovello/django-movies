from django.shortcuts import render
from .models import Genre, Movie, Rater, Ratings
from django.http import HttpResponse
from django.db.models import Count, Avg

# Create your views here.


def index(request):
    return render(request, 'movies/index.html')


def genres(request):
    genres = Genre.objects.all()
    all_genres = [str(genre) for genre in genres]
    return HttpResponse("<br />".join(all_genres))


def movies(request):
    movies = Movie.objects.all().order_by('title')
    return render(request, "movies/all_movies.html", {"movies":movies})

def toprated(request):
    top_20 = Movie.objects.annotate(top_rated=Avg('ratings__rating')).order_by('-top_rated')[:20]
    return render(request, 'movies/toprated.html', {"topmovies":top_20})

def movie(request, movie_id):
    movie = Movie.objects.get(movie_id=movie_id)
    users = movie.ratings_set.all()
    return render(request, "movies/movie.html", {"movie":movie, "users":users})

def users(request):
    users = Rater.objects.all()
    return render(request, "movies/users.html", {"users":users})

def user(request, uid):
    user = Rater.objects.get(number=uid)
    ratingse = user.ratings_set.all().order_by('movie__title', '-rating')
    excludes = Rater.objects.exclude(number = uid)
    recommend_movies = Movie.objects.filter(ratings__rater = uid, ratings__rating__gt = 3).order_by('title')[:20]
    return render(request, 'movies/user.html', {'user':user, "notwatched":recommend_movies, 'ratings':ratingse})

