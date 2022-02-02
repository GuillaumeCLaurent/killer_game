from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class Game_form(forms.Form):
    game_name = forms.CharField(label='Enter name:', max_length=100)

class Game_search(forms.Form):
    game_name = forms.CharField(label='Enter name:', max_length=100)

class Game_join(forms.Form):
    btn = forms.CharField()
