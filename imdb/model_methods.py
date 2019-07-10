from typing import Dict, List, Any, Union

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
RATING = [
    {"movie_id": 1, "no_of_ratings": 50000, "rating": 5},
    {"movie_id": 1, "no_of_ratings": 5000, "rating": 4},
    {"movie_id": 1, "no_of_ratings": 500, "rating": 3},
    {"movie_id": 1, "no_of_ratings": 50, "rating": 2},
    {"movie_id": 1, "no_of_ratings": 5, "rating": 1},
    {"movie_id": 2, "no_of_ratings": 40000, "rating": 5},
    {"movie_id": 2, "no_of_ratings": 4000, "rating": 4},
    {"movie_id": 2, "no_of_ratings": 400, "rating": 3},
    {"movie_id": 2, "no_of_ratings": 40, "rating": 2},
    {"movie_id": 2, "no_of_ratings": 4, "rating": 1},
    {"movie_id": 3, "no_of_ratings": 30000, "rating": 5},
    {"movie_id": 3, "no_of_ratings": 3000, "rating": 4},
    {"movie_id": 3, "no_of_ratings": 300, "rating": 3},
    {"movie_id": 3, "no_of_ratings": 30, "rating": 2},
    {"movie_id": 3, "no_of_ratings": 3, "rating": 1},
    {"movie_id": 4, "no_of_ratings": 20000, "rating": 5},
    {"movie_id": 4, "no_of_ratings": 2000, "rating": 4},
    {"movie_id": 4, "no_of_ratings": 200, "rating": 3},
    {"movie_id": 4, "no_of_ratings": 20, "rating": 2},
    {"movie_id": 4, "no_of_ratings": 2, "rating": 1},
    {"movie_id": 5, "no_of_ratings": 10000, "rating": 5},
    {"movie_id": 5, "no_of_ratings": 1000, "rating": 4},
    {"movie_id": 5, "no_of_ratings": 100, "rating": 3},
    {"movie_id": 5, "no_of_ratings": 10, "rating": 2},
    {"movie_id": 5, "no_of_ratings": 1, "rating": 1}
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


def create_rating():
    list_of_ratings = []
    for item in RATING:
        rating = MovieRating.objects.create(movie=Movie.objects.get(id=item["movie_id"]), rating=item["rating"],
                                            no_of_ratings=item["no_of_ratings"])
        list_of_ratings.append(rating)
    return list_of_ratings


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
    return {"name": actor.name, "gender": actor.gender, "date_of_birth": str(actor.date_of_birth),
            "unique_id": actor.unique_id}


def convert_movie_object_to_dict(movie):
    return {"movie_id": movie.id, "title": movie.title, "date_of_release": str(movie.date_of_release)}


def starts_with(title):
    return Movie.objects.filter(title__istartswith=title).values_list('title', flat=True)


def ends_with(title):
    return Movie.objects.filter(title__iendswith=title).values_list('title', flat=True)


def contains(title):
    return Movie.objects.filter(title__icontains=title).values_list('title', flat=True)


def top_paid_actor():
    movie_cast = MovieCast.objects.order_by('-remuneration_in_usd', 'cast__name')[0]
    return convert_actor_object_to_dict(movie_cast.cast)


def least_paid_actor():
    movie_cast = MovieCast.objects.order_by('remuneration_in_usd', 'cast__name')[0]
    return convert_actor_object_to_dict(movie_cast.cast)


def actors_born_in_a_month(month):
    actor_objects = Actor.objects.filter(date_of_birth__month=month).order_by('-date_of_birth')
    list_of_actors = []
    for actor in actor_objects:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def movies_casted_by_actors(unique_id):
    movie_ids = MovieCast.objects.filter(cast__unique_id=unique_id).order_by('-movie__date_of_release').values_list(
        'movie__id', flat=True).distinct()
    list_of_movies = []
    movie_objects = Movie.objects.filter(id__in=movie_ids)
    for movie in movie_objects:
        list_of_movies.append(convert_movie_object_to_dict(movie))
    return list_of_movies


def get_actor_by_month_and_role():
    actor_objects = Actor.objects.filter(date_of_birth__month=2, moviecast__role="heroine")
    list_of_actors = []
    for actor in actor_objects:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def get_actress_with_remuneration_in_between():
    actor_ids = MovieCast.objects.filter(remuneration_in_usd__lte=150000,
                                         remuneration_in_usd__gte=50000).order_by('cast__name').values_list('cast_id',
                                                                                                            flat=True).distinct()

    list_of_actors = []
    actor_objects = Actor.objects.filter(id__in=actor_ids)
    for actor in actor_objects:
        list_of_actors.append((convert_actor_object_to_dict(actor)))
    return list_of_actors


def get_actors_casted_in_movies():
    actor_ids = MovieCast.objects.filter(
        Q(movie__title='Titanic') | Q(movie__title='Avatar') | Q(movie__title='Endgame')).order_by(
        'remuneration_in_usd').values_list('cast_id', flat=True).distinct()
    list_of_actors = []
    actor_objects = Actor.objects.filter(id__in=actor_ids)
    for actor in actor_objects:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def get_actors_casted_in_particular_movies():
    actor_ids = MovieCast.objects.filter(
        (Q(movie__title='Titanic') | Q(movie__title='Avatar')) & (
                ~Q(movie__title='Inception') | ~Q(movie__title='Clash of titans'))).order_by(
        'remuneration_in_usd').values_list('cast_id', flat=True).distinct()
    actor_objects = Actor.objects.filter(id__in=actor_ids)
    list_of_actors = []
    for actor in actor_objects:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def all_the_actors_casted(list_of_movie_titles):
    list_of_actors = []
    actor_ids = MovieCast.objects.filter(movie__title__in=list_of_movie_titles).values_list('cast_id',
                                                                                            flat=True).distinct()
    actor_objects = Actor.objects.filter(id__in=actor_ids)
    for actor in actor_objects:
        list_of_actors.append(convert_actor_object_to_dict(actor))
    return list_of_actors


def complete_details_in_dict(moviecast, title):
    movie = Movie.objects.get(title=title)
    movie_cast_dictionary = {'movie': convert_movie_object_to_dict(movie)}\

    list_of_casts = []
    for movie_cast_obj in moviecast:
        cast_dictionary = {
            "actor": convert_actor_object_to_dict(movie_cast_obj.cast),
            "role": movie_cast_obj.role,
            "remuneration_in_usd": movie_cast_obj.remuneration_in_usd
        }
        list_of_casts.append(cast_dictionary)
    movie_cast_dictionary['cast'] = list_of_casts

    list_of_ratings = []
    for ratings in movie.movie_ratings.all():
        rating_dictionary = {"no_of_ratings": ratings.no_of_ratings,
                             "rating": ratings.rating
                             }
        list_of_ratings.append(rating_dictionary)
    movie_cast_dictionary["ratings"] = list_of_ratings

    return movie_cast_dictionary


def complete_movie_details(title):
    moviecast_query_set = MovieCast.objects.filter(movie__title=title)
    return complete_details_in_dict(moviecast_query_set, title)


def match_months():
    movie_ids = MovieCast.objects.filter(movie__date_of_release__month=F('cast__date_of_birth__month')).values_list(
        'movie__id', flat=True).distinct()
    movie_objects = Movie.objects.filter(id__in=movie_ids)
    list_of_movies = []
    for movie in movie_objects:
        list_of_movies.append(convert_movie_object_to_dict(movie))
    return list_of_movies


def movie_rating_more_than():
    movie_objects = Movie.objects.filter(movie_ratings__rating=5, movie_ratings__no_of_ratings__gte=20000)
    list_of_movies = []
    for movie in movie_objects:
        list_of_movies.append(convert_movie_object_to_dict(movie))
    return list_of_movies


def add_ratings():
    MovieRating.objects.filter(movie__actor__name="Robert Downey Jr", rating=1).update(
        no_of_ratings=F('no_of_ratings') + 100)
    return
