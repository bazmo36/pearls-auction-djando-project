from django import forms
from .models import Pearl

class PearlForm(forms.ModelForm):
    class Meta:
        model = Pearl
        fields = ["owner", "name", "description", "image", "created_at"]


