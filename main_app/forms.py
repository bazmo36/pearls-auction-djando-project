from django import forms
from .models import Pearl, Certification

class PearlForm(forms.ModelForm):
    class Meta:
        model = Pearl
        fields = ["name", "description", "image"]


class CertificationForm(forms.ModelForm):
    issued_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Certification
        fields = ['certified_by', 'certificate_number', 'grade', 'issued_at', 'certificate_image']
       
