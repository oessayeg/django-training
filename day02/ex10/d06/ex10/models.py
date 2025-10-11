from django.db import models


class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.TextField(blank=True, null=True)
    diameter = models.IntegerField(null=True)
    orbital_period = models.IntegerField(null=True)
    population = models.BigIntegerField(null=True)
    rotation_period = models.IntegerField(null=True)
    surface_water = models.FloatField(null=True)
    terrain = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=64, null=False)
    birth_year = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=32, blank=True, null=True)
    eye_color = models.CharField(max_length=32, blank=True, null=True)
    hair_color = models.CharField(max_length=32, blank=True, null=True)
    height = models.IntegerField(null=True)
    mass = models.FloatField(null=True)
    homeworld = models.ForeignKey(
        Planets,
        on_delete=models.CASCADE,
        null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)
    characters = models.ManyToManyField(People)

    def __str__(self):
        return self.title
