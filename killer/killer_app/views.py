from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from.models import Game

# Create your views here.
def index(request):
    game_list = Game.objects.order_by('name')
    context = {
        'game_list': game_list,
    }
    return render(request, 'killer_app/index.html', context)

def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'player_list': game.players,
    }
    return HttpResponse(f"You're looking at game {game_id}, named {game.name}.")

def results(request, game_id):
    return HttpResponse("You're looking at the results of game %s." % game_id)

def create(request, game_id):
    return HttpResponse("You're plaing in game %s." % game_id)




