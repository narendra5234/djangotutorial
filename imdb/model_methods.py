from imdb.models import *
from datetime import date
from django.db.models import Q, F

ACTORS = [
    {
        "name": "Robert Downey Jr",
        "gender": "male",
        "date_of_birth": date(1980, 3, 12),
        "unique_id": "1"
    },
    {
        "name": "Chris Hamsworth",
        "gender": "male",
        "date_of_birth": date(1990, 4, 15),
        "unique_id": "2"
    },
    {
        "name": "Sam",
        "gender": "male",
        "date_of_birth": date(1970, 5, 15),
        "unique_id": "3"
    },
    {
        "name": "Leonardo di caprico",
        "gender": "male",
        "date_of_birth": date(1997, 5, 22),
        "unique_id": "4"
    },
    {
        "name": "Joe Saldana",
        "gender": "female",
        "date_of_birth": date(1990, 5, 20),
        "unique_id": "5"
    },

]
MOVIES = [
    {
        "title": "Endgame",
        "date_of_release": date(2019, 1, 1)
    },
    {
        "title": "Inception",
        "date_of_release": date(2018, 2, 2)
    },
    {
        "title": "Avatar",
        "date_of_release": date(2017, 3, 3)
    },
    {
        "title": "Titanic",
        "date_of_release": date(2016, 4, 4)
    },
    {
        "title": "Clash of titans",
        "date_of_release": date(2010, 5, 5)
    }
]
CAST = [
    {
        "movie": {"title": "Endgame"},
        "cast": {
            "actor": {"unique_id": "1"},
            "role": "hero",
            "remuneration_in_usd": 50000
        },
    },
    {
        "movie": {"title": "Endgame"},
        "cast": {
            "actor": {"unique_id": "2"},
            "role": "hero",
            "remuneration_in_usd": 100000
        }
    },
    {
        "movie": {"title": "Inception"},
        "cast":
            {
                "actor": {"unique_id": "3"},
                "role": "hero",
                "remuneration_in_usd": 50000
            }

    },
    {
        "movie": {"title": "Inception"},
        "cast":
            {
                "actor": {"unique_id": "5"},
                "role": "heroine",
                "remuneration_in_usd": 150000
            }
    },
    {
        "movie": {"title": "Avatar"},
        "cast":
            {
                "actor": {"unique_id": "4"},
                "role": "hero",
                "remuneration_in_usd": 10000
            }
    },
    {
        "movie": {"title": "Titanic"},
        "cast":
            {
                "actor": {"unique_id": "4"},
                "role": "hero",
                "remuneration_in_usd": 10000
            }

    },
    {
        "movie": {"title": "Clash of titans"},
        "cast":
            {
                "actor": {"unique_id": "4"},
                "role": "hero",
                "remuneration_in_usd": 10000
            }

    }
]


def create_actor():
    list_of_actors = []
    for item in ACTORS:
        actor = Actor.objects.create(name=item["name"], gender=item["gender"], date_of_birth=item["date_of_birth"],
                                     unique_id=item["unique_id"])
        list_of_actors.append(actor)
    return list_of_actors


def create_movie():
    list_of_movies = []
    for item in MOVIES:
        movie = Movie.objects.create(title=item["title"], date_of_release=item["date_of_release"])
        list_of_movies.append(movie)
    return list_of_movies


def create_movie_cast():
    list_of_movie_cast = []
    for item in CAST:
        cast = MovieCast.objects.create(movie=Movie.objects.get(title=item["movie"]["title"]),
                                        cast=Actor.objects.get(unique_id=item["cast"]["actor"]["unique_id"]),
                                        role=item["cast"]["role"],
                                        remuneration_in_usd=item["cast"]["remuneration_in_usd"])
        list_of_movie_cast.append(cast)
    return list_of_movie_cast


def convert_actor_object_to_dict(actor):
    return {"name": actor.name, "gender": actor.gender, "date_of_birth": actor.date_of_birth,
            "unique_id": actor.unique_id}


def convert_moviecast_object_to_dict(moviecast_query_set):
    movie_cast_dictionary={}
    for moviecast in moviecast_query_set:
        movie_cast_dictionary['movie']=convert_movie_object_to_dict(moviecast.movie)
        list_of_casts=[]
        cast_dictionary={}
        for actor in moviecast.cast.all():
            cast_dictionary["actor"]= convert_actor_object_to_dict(actor)
            cast_dictionary["role"]=actor.moviecast_set.role
            cash_dictionary ["remuneration_in_usd"]=actor.moviecast_set.remuneration_in_usd
            list_of_casts.append(cast_dictionary)
        movie_cast_dictionary ['cast']=list_of_casts
    return movie_cast_dictionary 
 


def convert_movie_object_to_dict(movie):
    return {"movie_id": movie.id, "title": movie.title, "date_of_release": movie.date_of_release}


def starts_with(title):
    movie_query_set = Movie.objects.filter(title__istartswith=title)
    for movie_object in movie_query_set:
        return movie_object.title


def ends_with(title):
    movie_query_set = Movie.objects.filter(title__iendswith=title)
    for movie_object in movie_query_set:
        return movie_object.title


def contains(title):
    movie_query_set = Movie.objects.filter(title__icontains=title)
    for movie_object in movie_query_set:
        return movie_object.title


def top_paid_actor():
    movie_cast = MovieCast.objects.order_by('-remuneration_in_usd', 'cast__name')[0]
    return convert_actor_object_to_dict(movie_cast.cast)


def least_paid_actor():
    movie_cast = MovieCast.objects.order_by('remuneration_in_usd', 'cast__name')[0]
    return convert_actor_object_to_dict(movie_cast.cast)


def actors_born_in_a_month(month):
    actor_query_set = Actor.objects.filter(date_of_birth__month=month).order_by('-date_of_birth')
    list_of_actors = []
    for actor_object in actor_query_set:
        list_of_actors.append(convert_actor_object_to_dict(actor_object))
    return list_of_actors


def movies_casted_by_actors(unique_id):
    movie_cast = MovieCast.objects.filter(cast__unique_id=unique_id).order_by('-movie__date_of_release')
    list_of_movies = []
    for movie in movie_cast:
        print(movie.movie)
        list_of_movies.append(convert_movie_object_to_dict(movie.movie))
    return list_of_movies


def get_actor_by_month_and_role():
    actor_query_set = Actor.objects.filter(date_of_birth__month=2, moviecast__role="heroine")
    list_of_actors = []
    for actor in actor_query_set:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def get_actress_with_remuneration_in_between():
    moviecast_query_set = MovieCast.objects.filter(remuneration_in_usd__lte=150000,
                                                   remuneration_in_usd__gte=50000).order_by('cast__name')
    list_of_actors = []
    for moviecast in moviecast_query_set:
        list_of_actors.append((convert_actor_object_to_dict(moviecast.cast)))
    return list_of_actors


def get_actors_casted_in_movies():
    moviecast_query_set = MovieCast.objects.filter(
        Q(movie__title='Titanic') | Q(movie__title='Avatar') | Q(movie__title='Endgame')).order_by(
        'remuneration_in_usd')
    list_of_actors = []
    for moviecast in moviecast_query_set:
        list_of_actors.append(convert_actor_object_to_dict(moviecast.cast))
    return list_of_actors


def get_actors_casted_in_particular_movies():
    moviecast_query_set = MovieCast.objects.filter(
        (Q(movie__title='Titanic') | Q(movie__title='Avatar')) & (
                ~Q(movie__title='Inception') | ~Q(movie__title='Clash of titans'))).order_by(
        'remuneration_in_usd')
    list_of_actors = []
    for moviecast in moviecast_query_set:
        list_of_actors.append(convert_actor_object_to_dict(moviecast.cast))
    return list_of_actors


def all_the_actors_casted(list_of_movie_titles):
    unique_actors = []
    actor_id=[]
    for movie_title in list_of_movie_titles:
        moviecast_query_set = MovieCast.objects.filter(movie__title=movie_title)
        for moviecast in moviecast_query_set:
            actors_dict=convert_actor_object_to_dict(moviecast.cast)
            if actors_dict not in unique_actors:
                unique_actors.append(actors_dict)
    return unique_actors


def complete_movie_details(title):
    moviecast_query_set = MovieCast.objects.filter(movie__title=title)
    complete_details = []
    for moviecast in moviecast_query_set:
        complete_details.append(convert_moviecast_object_to_dict(moviecast))
    return complete_details


def match_months():
    moviecast_query_set = MovieCast.objects.filter(movie__date_of_release__month=F('cast__date_of_birth__month'))
    list_of_movies = []
    list_of_movies_id=[]
    for moviecast in moviecast_query_set:
        movie_id=moviecast.movie.id
        if movie_id not in list_of_movies_id:
            list_of_movies_id.append(movie_id)
            list_of_movies.append(convert_movie_object_to_dict(moviecast.movie))
    return list_of_movies
