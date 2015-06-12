from django.shortcuts import render, redirect
from .models import Genre, Movie, Rater, Ratings
from django.http import HttpResponse
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .forms import RaterForm, UserForm
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

def register(request):
    if request.method == "GET":
        user_form = UserForm()
        rater_form = RaterForm()
    elif request.method == "POST":
        user_form = UserForm(request.POST)
        rater_form = RaterForm(request.POST)
        if user_form.is_valid() and rater_form.is_valid():
            user = user_form.save()
            rater = rater_form.save()
            rater.user = user
            rater.save()

            password = user.password
            user.set_password(password)
            user.save()

            # Must call authenticate before login
            user = authenticate(username=user.username, password=password)
            login(request, user)
            messages.add_message(request,
                                 messages.SUCCESS, "KUDOS {} for making this far!".format(user.username))
            return redirect('index')
    return render(request, 'movies/register.html', {'userform':user_form, 'raterform':rater_form})
'''
def login(request):
    return render(request, 'movies/login.html')


'''
