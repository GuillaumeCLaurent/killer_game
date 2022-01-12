from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404

from .game_form import Game_form

from.models import Game, Player

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
        'player_list': [player for player in game.players.all()],
    }
    return render(request, 'killer_app/detail.html', context)#HttpResponse(f"You're looking at game {game_id}, named {game.name}.")

def results(request, game_id):
    return HttpResponse("You're looking at the results of game %s." % game_id)

def create(request, player_id):
    if request.method == 'GET':
        context = {
            'player': get_object_or_404(Player, pk=player_id),
            'is_created': False
        }

    elif request.method == 'POST':
        form = Game_form(request.POST)
        if form.is_valid():
            game = Game(name=form.cleaned_data['game_name'])
            game.save()
        else:
            print("not valid")
        context = {
            'player': get_object_or_404(Player, pk=player_id),
            'is_created': True
        }
    return render(request, 'killer_app/create.html', context)





