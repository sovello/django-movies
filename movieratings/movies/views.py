from django.shortcuts import render, redirect
from .models import Genre, Movie, Rater, Ratings
from django.http import HttpResponse
from django.db.models import Count, Avg
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import RaterForm, UserForm
from .forms import ContactForm, UserEditForm, RatingForm
from django.contrib.auth.decorators import login_required # so we can control access
from django.conf import settings # so we can access LOGIN_URL
from django.core.mail import send_mail, EmailMessage

# Create your views here.
            
def contact(request):
    # process form data if this is POST
    if request.method == 'POST':
        # this creates form instance and populates it with data
        form = ContactForm(request.POST)
        # first step is to check if form is valid
        if form.is_valid():
            # process form
            subjet = form.cleaned_data['subject']
            messagge = form.cleaned_data['message']
            sender = form.cleaned_data['email']
            cc_myself = form.cleaned_data['cc_myself']
            
            recipients = ['sovellohpmgani@gmail.com']
            if cc_myself:
                recipients.append(sender)

            email = EmailMessage(subject = subjet, body = messagge, from_email=sender, to=recipients)
            email.send()
            return HttpResponseRedirect('/movies')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form}) 


def index(request):
    movies_list = Movie.objects.all().order_by('title')
    movies = paginate(request, movies_list, 25, 'page')        
    return render(request, "movies/index.html", {"movies":movies})


def genres(request):
    genres = Genre.objects.all()
    all_genres = [str(genre) for genre in genres]
    return HttpResponse("<br />".join(all_genres))

#@login_required
def home(request):    
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    genres = [gn.name for gn in Genre.objects.all()]
    gnrs = Genre.objects.annotate(num_movies=Count('movie'))
    moviecounts = [gnrs[i].num_movies for i in range(len(gnrs))]
    avgrating = Genre.objects.annotate(avgrate=Avg('movie__ratings__rating'))
    fmale = Genre.objects.filter(movie__ratings__rater__gender__name__exact="Female").annotate(favg=Avg('movie__ratings__rating'))
    male = Genre.objects.filter(movie__ratings__rater__gender__name__exact="Male").annotate(mavg=Avg('movie__ratings__rating'))
    fmalerate = [round(fmale[i].favg,2) for i in range(len(fmale))]
    malerate = [round(male[i].mavg,2) for i in range(len(male))]
    avg = [round(avgrating[i].avgrate,2) for i in range(len(avgrating))]
    return render(request, 'movies/home.html', {"genres":genres, "moviecounts":moviecounts, 'avgrating':avg, 'malerating':malerate, "femalerating":fmalerate})

    
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
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    elif int(uid) == int(request.user.id) and  request.user.is_authenticated():
        user = Rater.objects.get(number=uid)
        ratings_list = user.ratings_set.all().order_by('movie__title', '-rating')
        paginatelist = paginate(request, ratings_list, 20, 'page')
        recommend_movies = Movie.objects.exclude(ratings__rater = uid).order_by('title')[:20]
        return render(request, 'movies/user.html', {'user':user, "notwatched":recommend_movies, 'ratings':paginatelist})
    
    elif request.user.is_authenticated() and uid != request.user.id:        
        user = Rater.objects.get(number=uid)
        ratings_list = user.ratings_set.all().order_by('movie__title', '-rating')
        paginatelist = paginate(request, ratings_list, 20, 'page')
        recommend_movies = Movie.objects.exclude(ratings__rater = uid).order_by('title')[:20]
        currUserMovies = Movie.objects.filter(ratings__rater = request.user.id)
        currUserMovies = [movie.movie_id for movie in currUserMovies]
        return render(request, 'movies/other_user.html', {'user':user, "notwatched":recommend_movies,
                                                          'ratings':paginatelist, 'currUserMovies':currUserMovies, 'uid':uid, 'ruid':request.user.id})


def userprofile(request, uid):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    userdata = Rater.objects.get(id=uid)
    if request.method == 'GET':
        userform = UserEditForm(instance=userdata)
        return render(request, 'movies/edit.html', {"thisuser":userform})
    elif request.method == 'POST':
        rater_form = UserEditForm(request.POST, request.FILES, instance = userdata)
        if rater_form.is_valid():         
            rater_form.save()
            return render(request, 'movies/index.html', {"message":"You successfully updated your profile"})


def rate(request, movie_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    movie = Movie.objects.get(pk=movie_id)
    if request.method == 'GET':
        rating_form = RatingForm()
        return render(request, 'movies/rate_movie.html', {"rateform":rating_form, "movie":movie})
    elif request.method == 'POST':
        rating = RatingForm(request.POST)
        if rating.is_valid():
            rating_save = rating.save(commit=False)
            rating_save.rater = Rater.objects.get(user__username = request.user)
            rating_save.movie = movie
            rating_save.save()
            messages.add_message(request,
                                 messages.SUCCESS, "You rated {}!".format(rating_save.rating))
        return redirect('user', rating_save.rater.id)

def editrating(request, rating_id):
    if not request.user.is_authenticated():
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    thisrating = Ratings.objects.get(id=rating_id)
    if request.method == 'GET':
        rating_form = RatingForm(instance=thisrating)
        return render(request, 'movies/edit_rating.html', {"rateform":rating_form, "ratingobj":thisrating})
    elif request.method == 'POST':
        updaterating = RatingForm(request.POST, instance = thisrating)
        if updaterating.is_valid():
            updaterating.save()
            messages.add_message(request,
                                 messages.SUCCESS, "You Updated the Rating to {}!".format(thisrating.rating))
        return redirect('user', thisrating.rater.id)
    
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
            return redirect('home')
    return render(request, 'movies/register.html', {'userform':user_form, 'raterform':rater_form})
