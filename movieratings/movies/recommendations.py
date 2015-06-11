import csv
import math

class MoviesData:
    '''Class to interact with the movie rating data set'''

    # container for movies (ids) and their respective rating
    # movie_rate_data[movie_id].append(review)
    movie_rate_data = {}

    # container for users and the ratings they did for each movie
    # user_rate_data[user_id] = {int(movie_id):int(review)}
    user_rate_data = {}

    # all movie titles
    movie_titles = {}

    # container holding user ids and respective movie ids only
    # user_movies[user_id].append(movie)
    user_movies = {}


    def __init__(self, rate_data_source, movie_data_source):
        '''Initialize the whole data set so you DRY'''

        with open(rate_data_source) as rating_data:
            rate_data = csv.reader(rating_data, delimiter='\t')
            for data in rate_data:
                if int(data[1]) in self.movie_rate_data:
                    self.movie_rate_data[int(data[1])].append(int(data[2]))
                else:
                    self.movie_rate_data[int(data[1])] = [int(data[2])]

                if int(data[0]) in self.user_rate_data:
                    self.user_rate_data[int(data[0])].update({int(data[1]):int(data[2])})
                    self.user_movies[int(data[0])].append(int(data[1]))
                else:
                    self.user_rate_data[int(data[0])] = {int(data[1]):int(data[2])}
                    self.user_movies[int(data[0])] = [int(data[1])]

        with open(movie_data_source, encoding='ISO-8859-1') as movie_data:
            movie_details = csv.reader(movie_data, delimiter='|')
            for movie in movie_details:
                if int(movie[0]) in self.movie_titles:
                    self.movie_titles[int(movie[0])].append(movie[1].split(','))
                else:
                    self.movie_titles[int(movie[0])] = movie[1].split(',')


    def movie_ratings(self, movie_id):
        '''Get ratings for a specific movie'''

        movie_title = self.movie_titles[movie_id][0]
        movie_ratings = sorted(self.movie_rate_data[movie_id], reverse=True)
        avg = round(sum(movie_ratings)/len(movie_ratings), 1)
        return (movie_title,len(movie_ratings),movie_ratings,avg)
        

    def movie_title(self, movie_id):
        '''Get the title for one particular movie'''

        return self.movie_titles[movie_id][0]


    def user_ratings(self, user_id):
        '''Get rating for all movies for a particular user
        Return it as {movieid:rating}
        '''

        return self.user_rate_data[user_id]


    def popular_movies(self, criteria):
        '''Return movies rated more than 20 times'''

        popular_movie = {}
        for movie in self.movie_rate_data:
            if len(self.movie_rate_data[movie]) >= criteria:
                popular_movie[movie] = round(sum(self.movie_rate_data[movie])/len(self.movie_rate_data[movie]), 1)
        return popular_movie


    def popular_movies_not_rated_by_person(self, user_id, criteria):
        '''Movies not rated by specific person'''

        not_rated_by = []
        for movie in self.popular_movies(criteria):
            if movie not in self.user_movies[user_id]:
                not_rated_by.append(self.movie_title(movie).split(','))
            else:
                pass
        if len(not_rated_by) == 0:
            return None
        else:
            return not_rated_by


    def ratings_by_two(self, first_user_id, second_user_id):
        '''get rating from two users for movies they have both seen
        This returns a tuple of lists holding corresponding ratings for specific
        movies
        '''

        user1 = []
        user2 = []
        for movie in self.user_rate_data[first_user_id]:
            if movie in self.user_rate_data[second_user_id]:
                # print("Movie {}:\n User {} rated {}: User {} rated {}".
                #         format(movie, first_user_id,self.user_rate_data[first_user_id][movie],
                #                 second_user_id,self.user_rate_data[second_user_id][movie]))
                user1.append(self.user_rate_data[first_user_id][movie])
                user2.append(self.user_rate_data[second_user_id][movie])
        return user1, user2


    def movies_recommended_to_user(self, current_user):
        '''Get movies to recommend to a user from similar users.'''

        movies_not_watched = []
        movies_user_has_watched = self.user_movies[current_user]
        for movie in self.user_movies:
            if movie not in movies_user_has_watched:
                movies_not_watched.append(movie)

        # get similarities between this user and the others
        # they have to have euclidean_distance of >= .7
        similarities = {}
        for user in self.user_movies:
            ratings = self.ratings_by_two(current_user, user)
            eu_distance = self.euclidean_distance(ratings[0], ratings[1])
            if eu_distance >= 0.5:
                similarities[user]=eu_distance

        # find movies watched by similar users, this user has not seen
        # for each user
        movies_to_recommend = {}
        for user in similarities:
            #for the movies they watched which ones this user has not seen
            #such that similarity * rating >= 4
            for movie_watched in self.user_movies[user]:
                similar_by = similarities[user]*self.user_rate_data[user][movie_watched]
                if movie_watched not in movies_not_watched and similar_by >= 4:
                    if user in movies_to_recommend:
                        movies_to_recommend[user].update({movie_watched:similar_by})
                    else:
                        movies_to_recommend[user] = {movie_watched:similar_by}

        recommended_movies = {}
        for user, movies in movies_to_recommend.items():
            for movie in movies:
                if movie not in recommended_movies:
                    recommended_movies[movie] = movies[movie]
        return recommended_movies

    def euclidean_distance(self,v, w):
        """Given two lists, give the Euclidean distance between them on a scale
        of 0 to 1. 1 means the two lists are identical.
        """
        # Guard against empty lists.
        if len(v) is 0:
            return 0

        differences = [v[idx] - w[idx] for idx in range(len(v))]
        squares = [diff ** 2 for diff in differences]
        sum_of_squares = sum(squares)

        return round(1 / (1 + math.sqrt(sum_of_squares)), 1)



if __name__ == '__main__':
    movie = MoviesData('data/u.data', 'data/u.item')
    print(movie.popular_movies(100))
    movie.movies_recommended_to_user(23)
