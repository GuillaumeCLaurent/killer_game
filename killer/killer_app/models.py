from django.db import models
from django.utils import timezone

# Create your models here.

class Player(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Game(models.Model):
    name = models.CharField(max_length=200)
    begin_date = models.DateTimeField('date published')
    players = models.ManyToManyField(Player)

    def is_recent(self):
        return self.begin_date >= timezone.now()
        
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

