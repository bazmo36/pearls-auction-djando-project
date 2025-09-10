from django import forms
from .models import Pearl, Certification, Bid
from django.core.exceptions import ValidationError

class PearlForm(forms.ModelForm):
    class Meta:
        model = Pearl
        fields = ["name", "description", "image", "color", "shape", "weight", "size", "origin"]


class CertificationForm(forms.ModelForm):
    issued_at = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Certification
        fields = ['certified_by', 'certificate_number', 'grade', 'issued_at', 'certificate_image']
       
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificate_image'].required = True


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.auction = kwargs.pop('auction', None)
        super().__init__(*args, **kwargs)

        if self.auction:
            min_bid = self.auction.get_min_next_bid()
            self.fields['amount'].widget.attrs.update({
                'min': min_bid,  
                'step': self.auction.get_next_bid_increment(),
                'placeholder': f"Min bid: {min_bid}"
            })

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if not self.auction:
            raise ValidationError("Auction context is missing.")

  
        if not self.auction.is_open():
            raise ValidationError("Auction is not currently open.")

    
        min_bid = self.auction.get_min_next_bid()
        if amount < min_bid:
            raise ValidationError(f"Your bid must be at least {min_bid}.")

        return amount