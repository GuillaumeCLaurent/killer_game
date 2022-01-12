from django.db import models
from django.utils import timezone

# Create your models here.

# Define Player model
class Player(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# Define Game model
class Game(models.Model):
    name = models.CharField(max_length=200)
    begin_date = models.DateTimeField('date published', null=True)
    players = models.ManyToManyField(Player)

    def is_recent(self):
        return self.begin_date >= timezone.now()
        
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

