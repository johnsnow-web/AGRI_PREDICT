# forms.py

from django import forms

class WeatherForm(forms.Form):
    location = forms.CharField(label='Location', max_length=100)
    plant = forms.CharField(label='Plant', max_length=100)
