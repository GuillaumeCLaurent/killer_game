from django.db import models

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=200)

class Game(models.Model):
    name = models.CharField(max_length=200)
    game_date = models.DateTimeField('date published')
    players = models.ManyToManyField(Player)
