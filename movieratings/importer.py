from django.db import models
import os
import django    

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movieratings.settings')
    import csv
    django.setup()

    from movies.models import Occupation, Gender, Genre, Movie, Rater, Ratings
    
    delimiter = ['\t', ',', '|']

    def readfile(filename, delim, encode='utf-8'):
        data = []
        with open(filename, encoding=encode) as datafile:
            filedata = csv.reader(datafile, delimiter=delim)
            for line in filedata:
                data.append(line)
        return data

    def getuserdata(filename):
        data = readfile(filename, '|')
        for line in data:
            print(line)

    def occupations(filename):        
        data = readfile(filename, ',')
        for idx, line in enumerate(data):
            occupation = Occupation()
            occupation.name = line[0].capitalize()
            occupation.occupation_id = idx+1       
            occupation.save()

            
    def gender():        
        for g in ['Female', 'Male']:
            gn = Gender()
            gn.name = g
            gn.save()


    def genres(filename):
        data = readfile(filename, '|')
        for line in data:            
            if len(line) == 0:
                continue
            genre = Genre()
            genre.name = line[0]
            genre.genre_id = line[1]
            genre.save()


    def movies(filename):
        data = readfile(filename, '|', encode='ISO-8859-1')        
        from dateutil.parser import parse
        
        for line in data:                              
            movie_data = line[0:5]
            print(movie_data)
            rating = line[5:]
            print(rating)
            movies = Movie()
            movies.movie_id = line[0]
            movies.title = line[1]
            movies.release_date = parse(line[2]).strftime('%Y-%m-%d')
            movies.video_release_date =  parse(line[3]).strftime('%Y-%m-%d')
            movies.imdb_url = line[4]
            movies.save()
            for idx, rate in enumerate(rating):
                if int(rate) == 1:
                    movies.genre.add(get_genre_object(idx))

            
    def get_genre_object(idx):
        obj = Genre.objects.get(pk=idx)
        return obj

    def raters(filename):
        data = readfile(filename, '|')
        for line in data:        
            rater = Rater()
            rater.age = line[1]
            rater.gender = Gender.objects.get(name__startswith=line[2])
            rater.occupation = Occupation.objects.get(name__startswith=line[3].capitalize())
            rater.zip_code = line[4]
            rater.number = int(line[0])
            rater.save()
            
            
    def ratings(filename):
        data = readfile(filename, '\t')       
        for line in data:        
            rate = Ratings()
            rate.rater = Rater.objects.get(number=int(line[0]))
            rate.movie = Movie.objects.get(movie_id=int(line[1]))
            rate.rating = int(line[2])
            rate.date = get_date(line[3])
            rate.save()
            print(line)
            
    def get_date(timestamp):
        import time
        return time.strftime("%Y-%m-%d", time.localtime(int(timestamp)))
    
    def main():
        occupations('data/u.occupation')
        gender()
        genres('data/u.genre')
        movies('data/u.item')
        raters('data/u.user')
        ratings('data/u.data')
    main()
