from django.db import models

# Create your models here.

class Occupation(models.Model):
    name = models.CharField(max_length = 140)

    def __str__(self):
        return '{}'.format(self.name)

    
class Gender(models.Model):
    name = models.CharField(max_length = 10)


    def __str__(self):
        return '{}'.format(self.name)

    
class Genre(models.Model):
    name = models.CharField(max_length = 140)

    
    def __str__(self):
        return '{}'.format(self.name)

    
class Movie(models.Model):
    title = models.CharField('Movie Title', max_length = 200)
    release_date = models.DateField('Release Date')
    video_release_date = models.DateField('Video Release Date')
    imdb_url = models.CharField('IMDB URL', max_length = 250)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return '{}'.format(self.title)


class Rater(models.Model):
    age = models.IntegerField()
    gender = models.ForeignKey(Gender)
    occupation = models.ForeignKey(Occupation)
    zip_code = models.CharField('Zip Code', max_length = 20)

    def __str(self):
        return '{} - {}'.format(self.gender, self.occupation)

    
class Ratings(models.Model):
    rater = models.ForeignKey(Rater)
    movie = models.ForeignKey(Movie)
    rating = models.IntegerField()

    def __str__(self):
        return '{}:{} -> {}'.format(self.movie, self.rating, self.rater)
