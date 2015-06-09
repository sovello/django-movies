from django.contrib import admin
from .models import *
# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    '''Tweak the display of the admin forms'''
    # This line chages the order of display of fields
    fields = ['title', 'genre', 'imdb_url', 'release_date', 'video_release_date']

    # This line changes the order fields are display on the view form
    list_fields = ('title', 'release_date', 'imdb_url')

    
admin.site.register(Occupation)
admin.site.register(Gender)
admin.site.register(Genre)
admin.site.register(Ratings)
admin.site.register(Movie, MovieAdmin) # add this for the change to take effect
admin.site.register(Rater)
