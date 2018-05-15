from django.forms import ModelForm
from django import forms
from web.models import Unit

class UnitForm(ModelForm):
    class Meta:
        model = Unit
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Nome da nova unidade'}) 
        }