
from django import forms
from .models import People

class SearchForm(forms.Form):
    min_release_date = forms.DateField(label='Movies minimum release date', required=False)
    max_release_date = forms.DateField(label='Movies maximum release date', required=False)
    min_diameter = forms.IntegerField(label='Planet diameter greater than', required=False)
    gender = forms.ChoiceField(
        label='Character gender',
        choices=People.GENDER_CHOICES,
        required=False
    )
