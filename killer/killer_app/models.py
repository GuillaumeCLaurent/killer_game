from logging import NullHandler
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string 

# Create your models here.
def id_generator(size=6, chars= string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
# Define Game model
class Game(models.Model):
    name = models.CharField(max_length=200)
    begin_date = models.DateTimeField('date published', null=True)
    users = models.ManyToManyField(User)
    is_started = models.BooleanField(default=False)
    is_finsished = models.BooleanField(default=False)
    winner = models.CharField(max_length=200, null=True)

    unique_id = models.CharField(max_length=6, null=True, blank=True, unique=True)

    # Sample of an ID generator - could be any string/number generator
    # For a 6-char field, this one yields 2.1 billion unique IDs
    
    def save(self): 
        if not self.unique_id:
            # Generate ID once, then check the db. If exists, keep trying.
            self.unique_id = id_generator()
            while Game.objects.filter(unique_id=self.unique_id).exists():
                self.unique_id = id_generator()
        super(Game, self).save()

    def is_ready(self):
        for user in self.users.all():
            if not user.player.action :
                return False
        return True

    def stop(self):
        for user in self.users.all():
            user.player.quit_game()
            user.save()
        self.is_started = False    

    def start(self):

        print("Starting")        
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

            list[i][1].player.target_name = list[ind1][1].player.player_name
            list[i][1].player.target_id = list[ind1][1].id

            list[ind1][1].player.chaser_name = list[i][1].player.player_name
            list[ind1][1].player.chaser_id = list[i][1].id

            list[i][1].save()
            print(list[i][1].player.target_action, list[i][1].player.target_name)

        self.is_started = True
        self.is_finsished = False
        self.save()

    def kill_player(self, ukiller, ukilled):
        

        if not self.check_end():

            ukiller.player.target_name = ukilled.player.target_name
            ukiller.player.target_action = ukilled.player.target_action
            ukiller.save()
        
        else:
            self.is_finished = True
            self.is_started = False
            self.winner = ukiller.player.player_name
            self.save()

        ukilled.player.reset()
        ukilled.save()
    
    def player_discovered(self, user, user_chaser, user_target):
        

        if not self.check_end():
            user_chaser.player.taget_name = user_target.player.player_name
            user_chaser.player.target_id = user_target.id

            user_target.player.chaser_name = user_chaser.player.player_name
            user_target.player.chaser_id = user_chaser.id
            
        
        user_chaser.save()

        user.player.reset()
        user.save()



    def check_end(self):
        users_list = [user for user in self.users.all()]
        false_counter = 0
        winner = users_list[0]
        for user in users_list:
            if user.player.is_alive :
                winner = user.player.player_name
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

    player_name = models.CharField(max_length=200, null=True)
    is_in_game = models.BooleanField(default=False)

    action = models.CharField(max_length=200, null=True)
    target_name = models.CharField(max_length=200, null=True)
    target_id = models.IntegerField(null=True)
    target_action = models.CharField(max_length=200, null=True)

    chaser_name = models.CharField(max_length=200, null=True)
    chaser_id = models.IntegerField(null=True)

    created = models.ForeignKey(Game, on_delete=models.CASCADE, null=True)
    is_alive = models.BooleanField(default=True)


    def reset(self):
        self.action = None
        self.target_action = None
        self.target_name = None
        self.target_id = None
        self.chaser_id = None
        self.chaser_name = None

    def quit_game(self):
        self.reset()
        self.is_in_game = False
        self.player_name = None
    
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



