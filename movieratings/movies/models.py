from django.db import models
from django.utils.html import format_html
from django.db.models import Avg

# Create your models here.

class Occupation(models.Model):
    occupation_id = models.CharField(primary_key=True, max_length=100, default=1)
    name = models.CharField(max_length = 140)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Occupation'
    
class Gender(models.Model):
    name = models.CharField(max_length = 10)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name_plural = 'Gender'

        
class Genre(models.Model):
    genre_id = models.IntegerField(primary_key=True, default=0)
    name = models.CharField(max_length = 140)

    def __str__(self):
        return '{}'.format(self.name)

    def total_movies(self): # return the number of counts each user has made
        return self.movie_set.count()
    
    
class Movie(models.Model):
    title = models.CharField('Movie Title', max_length = 200)
    release_date = models.DateField('Release Date')
    video_release_date = models.DateField('Video Release Date')
    imdb_url = models.CharField('IMDB URL', max_length = 250)
    genre = models.ManyToManyField(Genre)
    movie_id = models.IntegerField('Movie ID',primary_key=True, default=10000)

    def __str__(self):
        return '{}'.format(self.title)

    def hyperlink(self):
        '''Need to import format_html above, so you can create this URL'''
        return format_html('<a target="_blank" href="{}">{}</a>', self.imdb_url, self.title)

    def rate_counts(self):
        return self.ratings_set.count()

    def average_rating(self):
        average = self.ratings_set.all().aggregate(Avg('rating'))
        return round(average['rating__avg'], 1)
    
    hyperlink.allow_tags = True #use this for Django to format to HTML

    
class Rater(models.Model):
    age = models.IntegerField()
    gender = models.ForeignKey(Gender)
    occupation = models.ForeignKey(Occupation)
    zip_code = models.CharField('Zip Code', max_length = 20)
    number = models.IntegerField('Rater Number', default=10000)

    def __str__(self):
        return '{} (ID #:{})'.format(self.occupation, self.number)
    
    def rated_movies(self): # return the number of counts each user has made
        return self.ratings_set.count()
    
    
class Ratings(models.Model):
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{} -> {}'.format(self.movie, self.rating, self.rater)

    class Meta:
        verbose_name_plural = 'Ratings'
