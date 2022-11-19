from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields #+ ("email",)

class Game_form(forms.Form):
    game_name = forms.CharField(label='Enter name:', max_length=100)

class Game_search(forms.Form):
    game_name = forms.CharField(label='Enter name:', max_length=100)

class Game_join(forms.Form):
    btn = forms.CharField()

class Action_form(forms.Form):
    action = forms.CharField(label="Enter your action", max_length=200)

class Name_form(forms.Form):
    name = forms.CharField(label="Enter your player name", max_length=200)

class Game_search_form(forms.Form):
    search = forms.CharField(label='Search', max_length=100)
