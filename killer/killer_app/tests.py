import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Game, Player
from django.db import models
from django.contrib.auth.models import User


# Create your tests here.
class GameModelTests(TestCase):

    def setUp(self):
        n = 10
        self.test_game = Game(name="test_game")#pub_date=time)
        self.test_game.save()
        self.users = [User(username=f"player{i}") for i in range(n)]


    def test_players_matchmaking(self):
        """
        is_recent() returns False for games whose begin_date is in the future.
        """
        for user in self.users:
            user.player = Player()
            user.player.action=f"Action from {user.username}"
            #user.player.action = models.CharField(f"Action from {user.username}")
            #user.player.save()
            user.save()
            self.test_game.save()
            print(user.player.action)
    
            self.test_game.users.add(user)

        
        self.test_game.save()
        self.test_game.start()
        
        for user in self.users:
            user.save()
            #self.assertIsNot(user.player.target_action, None)
            #self.assertIsNot(user.player.target_name, None)
            if self.test_game.is_started:
                print(f"{user.username} : Action : {user.player.target_action} Target : {user.player.target_name}")
        
        #self.assertIs(future_game.is_recent(), False)

    

