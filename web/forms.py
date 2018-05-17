from django.forms import ModelForm
from django import forms
from web.models import Unit, Local

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome da nova unidade'}) 
        }


class LocalForm(ModelForm):
    class Meta:
        model = Local
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome do novo local'})
        }