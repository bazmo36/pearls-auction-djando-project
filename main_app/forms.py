from django import forms
from .models import Pearl

class PearlForm(forms.ModelForm):
    class Meta:
        model = Pearl
        fields = ["name", "description", "image"]


