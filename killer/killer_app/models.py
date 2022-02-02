from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.



# Define Player model
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_in_game = models.BooleanField(default=False)
    target_name = models.CharField(max_length=200, null=True)
    target_action = models.CharField(max_length=200, null=True)

    #name = models.CharField(max_length=200)
    """
    class Meta:
        ordering = ['user.username']
    """
    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()


# Define Game model
class Game(models.Model):
    name = models.CharField(max_length=200, unique = True)
    begin_date = models.DateTimeField('date published', null=True)
    users = models.ManyToManyField(User)
    #creator = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

