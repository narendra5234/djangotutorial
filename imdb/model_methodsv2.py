from typing import Dict, List, Any, Union
from imdb.models import *
from datetime import date
from django.db.models import *

ACTORS = [
    {
        "name": "Robert Downey Jr",
        "gender": "male",
        "date_of_birth": date(1980, 3, 12),
        "unique_id": "1",
        "born_in_country": "Washington"
    },
    {
        "name": "Chris Hamsworth",
        "gender": "male",
        "date_of_birth": date(1990, 4, 15),
        "unique_id": "2",
        "born_in_country": "London"
    },
    {
        "name": "Tom",
        "gender": "male",
        "date_of_birth": date(1970, 5, 15),
        "unique_id": "3",
        "born_in_country": "New York"
    },
    {
        "name": "Leonardo di caprico",
        "gender": "male",
        "date_of_birth": date(1997, 5, 22),
        "unique_id": "4",
        "born_in_country": "Delhi"

    },
    {
        "name": "Joe Saldana",
        "gender": "female",
        "date_of_birth": date(1990, 5, 20),
        "unique_id": "5",
        "born_in_country": "Los Vegas"
    }
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


def date_format(date):
    return date.strftime("%d-%m-%Y")


def get_list_of_movies(list_of_dictionary):
    list_of_movies = []
    for item in list_of_dictionary:
        movie_dictionary = {
            "movie_id": item["id"],
            "title": item["title"],
            "date_of_release": date_format(item["date_of_release"])
        }
        list_of_movies.append(movie_dictionary)
    return list_of_movies


def create_actor():
    list_of_actors = []
    for item in ACTORS:
        actor = Actor.objects.create(name=item["name"], gender=item["gender"], date_of_birth=item["date_of_birth"],
                                     unique_id=item["unique_id"], born_in_country=item["born_in_country"])
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


def max_actor_movies():
    return get_list_of_movies(list(
        Movie.objects.annotate(actor_count=Count('actors')).order_by('-actor_count', 'title').values('id', 'title',
                                                                                                     'date_of_release')))


def get_remuneration_stats(movie_id):
    return MovieCast.objects.filter(movie_id=movie_id).aggregate(avg_remuneration=Avg('remuneration_in_usd'),
                                                                 min_remuneration=Min('remuneration_in_usd'),
                                                                 max_remuneration=Max('remuneration_in_usd'))


def get_min_age_of_cast_in_movie():
    return list(Movie.objects.annotate(min_age=Max('actors__date_of_birth')).values('title', 'min_age'))


def get_movies_that_doesnot_have_heroine():
    return get_list_of_movies(
        list(Movie.objects.filter(~Q(movie_cast__role="heroine")).values('id', 'title', 'date_of_release')))


def get_movies_more_than_ten_female():
    return list(MovieCast.objects.values('movie__id').annotate(
        actor_count=Count('cast__gender', filter=Q(cast__gender='female'))).filter(actor_count__gt=10).values(
        'movie__id', 'movie__title', 'movie__date_of_release'))


def diff_between_male_and_female():
    return list(Movie.objects.annotate(male_count=Count('actors__gender', filter=Q(actors__gender="male")),
                                       female_count=Count('actors__gender', filter=Q(actors__gender="female")),
                                       ).annotate(diff_count=F('male_count') - F('female_count')).order_by(
        '-diff_count').values('title', 'diff_count'))


def get_movie_contains_title():
    return get_list_of_movies(
        list(Movie.objects.filter(actors__name__icontains="tom").annotate(actors_count=Count('actors')).values('id',
                                                                                                               'title',
                                                                                                               'date_of_release',
                                                                                                               'actors_count')))


def avg_remuneration_by_actors():
    return get_list_of_movies(
        list(Movie.objects.filter(movie_ratings__no_of_ratings__gt=10000, movie_ratings__rating=5).annotate(
            avg_remuneration=Avg('movie_cast__remuneration_in_usd')).values('id', 'title', 'date_of_release')))


def no_of_actors_same_month():
    return list(Actor.objects.values('date_of_birth__month').annotate(actor_count=Count('date_of_birth__month')).filter(
        actor_count__gte=2).values('actor_count'))


def no_of_actors_same_year():
    return list(Actor.objects.values('date_of_birth__year').annotate(actor_count=Count('date_of_birth__year')).filter(
        actor_count__gte=2).values('actor_count'))


def no_of_actors_same_name():
    return list(Actor.objects.values('name').annotate(actor_count=Count('name')).filter(
        actor_count__gte=2).values('actor_count'))
