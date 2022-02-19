from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, Http404
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
#from js2py import require

from .Forms import Game_form, CustomUserCreationForm, Action_form, Game_search_form

from.models import Game, Player

# Create your views here.
def index(request):
    user = request.user

    if user.is_authenticated:
        game =  user.game_set.all()
        print(game)
        if game:
            print(game[0].id)
            context = {
                'game_id' :game[0].id,
                'game_name' : game[0].name,
            }
            return render(request, 'killer_app/index.html', context)
            
    context = {
        'game' :None,
    }

    return render(request, 'killer_app/index.html', context)

def register(request):
    if request.method == "GET":
        return render(
            request, "killer_app/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))
        return redirect(reverse("index"))
    else:
        return redirect(reverse("index"))


def detail(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    user = request.user

    if request.method == 'POST':
        
        form = Action_form(request.POST)
        if form.is_valid():
            act = form.cleaned_data['action'] 
            if act != 'Your action':
                user.player.action = form.cleaned_data['action'] 

        if 'join' in request.POST:
            game.users.add(user)
            request.user.player.is_in_game = True
            
        if 'kill' in request.POST:
            print()
            game.kill_player(user, game.users.filter(username=user.player.target_name)[0])

        if 'start' in request.POST:
            game.start()

        
        if 'stop' in request.POST:
            game.stop()        

        if 'quit' in request.POST:
            game.users.remove(user)
            request.user.player.is_in_game = False
            if game == user.player.created:
                user.player.created = None
           
        
        user.save()
        game.save()
        

    #is_in_game = request.user in  game.users.all()
    context = {
        'player_list': [(user.username, user.player.is_alive) for user in game.users.all()],
        'game': game, 
        'is_in_game': request.user in game.users.all(),
        'is_admin': user.player.created == game,
        'is_ready': game.is_ready(), 
        
    }
    

    return render(request, 'killer_app/detail.html', context)#HttpResponse(f"You're looking at game {game_id}, named {game.name}.")


def results(request, game_id):
    return HttpResponse("You're looking at the results of game %s." % game_id)

def create(request):
    if request.method == 'GET':
        context = {
            #'player': get_object_or_404(Player, pk=player_id),
            #'is_created': False
        }

    elif request.method == 'POST':
        form = Game_form(request.POST)
        if form.is_valid():
            request.user.player.is_in_game = True
            game = Game(name=form.cleaned_data['game_name'])
            game.save()
            game.users.add(request.user)
            request.user.player.created = game
            request.user.player.is_in_game = True
            request.user.save()
            

        else:
            print("not valid")
        context = {
            #'player': get_object_or_404(Player, pk=player_id),
            #'is_created': True
        }
    return render(request, 'killer_app/create.html', context)


def join(request):
    if request.method == 'POST':
        form = Game_search_form(request.POST)
        if form.is_valid():
            game_list = Game.objects.filter(name=form.cleaned_data['search'])
        else:
            game_list = Game.objects.order_by('name')
    else:
        game_list = Game.objects.order_by('name')
    
    context = {
        'game_list': game_list,
    }
    return render(request, 'killer_app/join.html', context)


