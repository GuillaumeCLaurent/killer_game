from logging import NullHandler
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

# Create your models here.

# Define Game model
class Game(models.Model):
    name = models.CharField(max_length=200, unique = True)
    begin_date = models.DateTimeField('date published', null=True)
    users = models.ManyToManyField(User)
    is_started = models.BooleanField(default=False)
    is_finsished = models.BooleanField(default=False)
    winner = models.CharField(max_length=200, null=True)


    def is_ready(self):
        for user in self.users.all():
            if not user.player.action :
                return False
        return True


    def stop(self):
        for user in self.users.all():
            user.player.target_name = None
            user.player.target_action = None
            user.save()
        self.is_started = False
            

    def start(self):
        
        actions_list = [str(user.player.action) for user in self.users.all()]
        users_list = [user for user in self.users.all()]

        for user in users_list:
            user.player.is_alive = True
        
        list = [elmt for elmt in zip(actions_list, users_list)]

        random.shuffle(list)
        n = len(actions_list)

        for i in range(n):
            ind1 = (i+1)%n
            ind2 = (i-1)%n
            #res[list[i][1]] = (list[ind1][1], list[ind2][0])
            list[i][1].player.target_action = list[ind2][0]
            list[i][1].player.target_name = list[ind1][1].username
            list[i][1].save()

        self.is_started = True
        self.is_finsished = False
        self.save()

    def kill_player(self, ukiller, ukilled):
        ukilled.player.is_alive = False
        ukilled.save()

        if not self.check_end():

            ukiller.player.target_name = ukilled.player.target_name
            ukiller.player.target_action = ukilled.player.target_action
            ukiller.save()
        
        else:
            self.is_finished = True
            self.is_started = False
            self.save()

    
    def check_end(self):
        users_list = [user for user in self.users.all()]
        false_counter = 0
        winner = users_list[0]
        for user in users_list:
            if user.player.is_alive :
                winner = user.username
                false_counter = false_counter + 1

        if false_counter <= 1:
            self.winner = winner
            return True

        return False

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name



# Define Player model
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    is_in_game = models.BooleanField(default=False)
    action = models.CharField(max_length=200, null=True)
    target_name = models.CharField(max_length=200, null=True)
    target_action = models.CharField(max_length=200, null=True)
    created = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    is_alive = models.BooleanField(default=True)


    """
    class Meta:
        ordering = ['user.username']
    """
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_player(sender, instance, **kwargs):
    instance.player.save()



