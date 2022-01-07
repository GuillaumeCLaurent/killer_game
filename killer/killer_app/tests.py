import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Game, Player

# Create your tests here.
class GameModelTests(TestCase):

    def test_is_recent_with_future_game(self):
        """
        is_recent() returns False for games whose begin_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_game = Game(pub_date=time)
        self.assertIs(future_game.is_recent(), False)
