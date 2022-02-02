from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include("django.contrib.auth.urls")),
    path("register/", views.register, name="register"),
    path('<int:game_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:game_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('create/', views.create, name='create'),
    path('join/', views.join, name='join'),
]

