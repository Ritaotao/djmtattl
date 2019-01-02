# djmtattl/turnstile/forms.py

from django.forms import ModelForm, TextInput
from .models import Station

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class' : 'input', 'placeholder' : 'Station Name'}),
        } #updates the input class to have the correct Bulma class and placeholder