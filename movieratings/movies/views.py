from django.shortcuts import render, redirect
from .models import Genre, Movie, Rater, Ratings
from django.http import HttpResponse
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RaterForm, UserForm
from django.contrib.auth.decorators import login_required # so we can control access
from django.conf import settings # so we can access LOGIN_URL
# Create your views here.


def index(request):
    return render(request, 'movies/index.html')


def genres(request):
    genres = Genre.objects.all()
    all_genres = [str(genre) for genre in genres]
    return HttpResponse("<br />".join(all_genres))

#@login_required
def movies(request):
    movies_list = Movie.objects.all().order_by('title')
    movies = paginate(request, movies_list, 25, 'page')        
    return render(request, "movies/all_movies.html", {"movies":movies})


def paginate(request, items_list, n_per_page, var):
    paginator = Paginator(items_list, n_per_page) # only show 30 movies
    page = request.GET.get(var) # page has to be set in the url
    try:
        items = paginator.page(page)
    except PageNotAnInteger: # if page is not an integer, default to first page       
        items = paginator.page(1)
    except EmptyPage: # page is out of range
        items = paginator.page(paginator.num_pages)
    return items


def toprated(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    top_20 = Movie.objects.annotate(top_rated=Avg('ratings__rating')).order_by('-top_rated')[:20]
    return render(request, 'movies/toprated.html', {"topmovies":top_20})

def movie(request, movie_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    movie = Movie.objects.get(movie_id=movie_id)
    users_list = movie.ratings_set.all()
    users = paginate(request, users_list, 20, 'page')
    return render(request, "movies/movie.html", {"movie":movie, "users":users})

def users(request):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    users_list = Rater.objects.all()
    users = paginate(request, users_list, 25, 'page')
    return render(request, "movies/users.html", {"users":users})

def user(request, uid):
    user = Rater.objects.get(number=uid)
    ratings_list = user.ratings_set.all().order_by('movie__title', '-rating')
    excludes = Rater.objects.exclude(number = uid)
    ratingse = paginate(request, ratings_list, 20, 'page')
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

def rate(request, movie_id):
    return render(request, 'movies/rate_movie.html')
