from django.contrib import admin
from .models import *

# Register your models here.

class MovieAdmin(admin.ModelAdmin):
    '''Tweak the display of the admin forms'''
    # This line chages the order of display of fields
    fields = ['title', 'genre', 'imdb_url', 'release_date', 'video_release_date']

    # This line changes the order fields are display on the view form
    list_display = ('title', 'release_date', 'hyperlink')

    #add/change the filters
    list_filter = ['release_date', 'genre']
    # to include search
    search_fields = ['title']


class RaterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'rated_movies')
    #search_fields = ['occupation'] seems not to work with mapped fields

    list_filter = ['occupation']

    
class GenreAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total_movies')


class OccupationAdmin(admin.ModelAdmin):
    list_display = ('__str__') #, 'admin_order_field = -name')

    
admin.site.register(Occupation)
admin.site.register(Gender)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Ratings)
admin.site.register(Movie, MovieAdmin) # add this for the change to take effect
admin.site.register(Rater, RaterAdmin)
