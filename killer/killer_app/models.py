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

    def stop(self):
        for user in self.users.all():
            user.player.target_name = None
            user.player.target_action = None
            user.save()
            

    def start(self):

        actions_list = [str(user.player.action) for user in self.users.all()]
        users_list = [user for user in self.users.all()]
        
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
          
        """
        n = len(al)
        #res = {}
        ind_l= [i for i in range(0, n)]

        ind = random.choice(ind_l)
        first_ind = ind
        ind_l.remove(ind)

        while(len(ind_l)>1):  
    
            sec_ind = random.choice(ind_l)
            #res[pl[ind]] = (al[sec_ind], pl[sec_ind])
            pl[ind].player.target_action = al[sec_ind]
            pl[ind].player.target_name = pl[sec_ind].username
            pl[ind].save()
            ind = sec_ind
            ind_l.remove(ind)
        
        
        #res[pl[ind_l[0]]] = (al[first_ind], pl[first_ind])
        pl[ind].player.target_action = al[first_ind]
        pl[ind].player.target_name = pl[first_ind].username
        pl[ind].save()
        #return res
        """

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



