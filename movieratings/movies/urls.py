from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^genres', views.genres, name='genres'),
    url(r'^movies', views.movies, name='movies'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.movie, name="movie"),
    url(r'^toprated/$', views.toprated, name='toprated'),
    url(r'^users', views.users, name='users'),
    url(r'^user/(?P<uid>[0-9]+)/$', views.user, name='user')
]