from imdb.models import *
from datetime import date

ACTORS = [
    {
        "name": "Mahesh",
        "gender": "male",
        "date_of_birth": date(1980, 3, 12),
        "unique_id": "1"
    },
    {
        "name": "Allu Arjun",
        "gender": "male",
        "date_of_birth": date(1990, 4, 15),
        "unique_id": "2"
    },
    {
        "name": "Balayya Babu",
        "gender": "male",
        "date_of_birth": date(1970, 5, 15),
        "unique_id": "3"
    }, {
        "name": "Akhil",
        "gender": "male",
        "date_of_birth": date(1997, 5, 22),
        "unique_id": "4"
    }

]


def create_actor(ACTORS):
    for item in ACTORS:
        actor = Actor.objects.create(name=item["name"], gender=item["gender"], date_of_birth=item["date_of_birth"],
                                     unique_id=item["unique_id"])
    return actor


def create_movie(title, date_of_release):
    movie = Movie.objects.create(title=title, date_of_release=date_of_release)
    return movie
