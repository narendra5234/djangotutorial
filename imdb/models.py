from django.core.validators import *
from django.db import models
from django.db.models import Q, F, FloatField, OuterRef, Subquery
from django.db.models import Sum, Count


class Actor(models.Model):
    name = models.TextField()
    gender = models.TextField()
    date_of_birth = models.DateField()
    unique_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.TextField()
    date_of_release = models.DateField()
    actor = models.ManyToManyField(Actor, through='MovieCast')

    def __str__(self):
        return self.title


class MovieCast(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='movie_cast')
    cast = models.ForeignKey(Actor, on_delete=models.CASCADE)
    role = models.TextField()
    remuneration_in_usd = models.FloatField()


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='movie_ratings')
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    no_of_ratings = models.IntegerField()
