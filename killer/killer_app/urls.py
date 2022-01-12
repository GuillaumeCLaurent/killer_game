from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('<int:game_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:game_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:player_id>/create/', views.create, name='create'),
]

