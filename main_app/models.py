from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError



# Create your models here.


class Pearl(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pearls")
    name= models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="pearls/")
    created_at = models.DateTimeField(auto_now_add=True)


    color = models.CharField(max_length=50, blank=True, null=True)
    shape = models.CharField(max_length=50, blank=True, null=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Weight in grams")
    size = models.CharField(max_length=50, blank=True, null=True)
    origin = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} (owned by {self.owner.username})"
    


class Certification(models.Model):

    GRADE_CHOICES = [
        ('A', 'A - Excellent Quality'),
        ('AA', 'AA - Very High Quality'),
        ('AAA', 'AAA - Highest Quality'),
        ('B', 'B - Good'),
        ('C', 'C - Commercial Grade'),
    ]
     
    pearl = models.ForeignKey(Pearl, related_name='certifications', on_delete=models.CASCADE)
    certified_by = models.CharField(max_length=100)
    certificate_number = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES)
    issued_at = models.DateField(null=True, blank=True)
    certificate_image = models.ImageField(upload_to='certificates/')

    def __str__(self):
        return f"Certificate {self.certificate_number} for {self.pearl.name}"



class AuctionListing(models.Model):
    pearl = models.OneToOneField("Pearl", on_delete=models.CASCADE, related_name="auction")
    reserve_price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_sold = models.BooleanField(default=False)
    last_bid_time = models.DateTimeField(null=True, blank=True)


    def start_time(self):
        created_date = self.created_at
        days_ahead = 0 - created_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return (created_date + timedelta(days=days_ahead)).replace(hour=0, minute=0, second=0, microsecond=0)

    def end_time(self):
        return self.start_time().replace(hour=23, minute=59, second=59)

    def is_open(self):
        now = timezone.now()
        return self.start_time() <= now <= self.end_time()

    def can_modify(self):
        return timezone.now() < self.start_time()

    def current_price(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.amount if highest_bid else 0

    def current_winner(self):
        highest_bid = self.bids.order_by('-amount').first()
        return highest_bid.bidder if highest_bid else None

    def get_next_bid_increment(self):
        price = self.current_price()

        if price < 500:
            return 25
        elif price < 1000:
            return 50
        elif price < 5000:
            return 100
        elif price < 10000:
            return 250
        elif price < 25000:
            return 500
        elif price < 50000:
            return 1000
        elif price < 100000:
            return 2500
        elif price < 250000:
            return 5000
        elif price < 500000:
            return 10000
        elif price < 1000000:
            return 25000
        else:
            return 50000

    def get_min_next_bid(self):

        if self.current_price() == 0:
            return max(self.reserve_price, 0)
        return self.current_price() + self.get_next_bid_increment()

    def has_met_reserve(self):
        return self.current_price() >= self.reserve_price

    def status(self):
        now = timezone.now()
        if self.is_sold:
            return "Sold"
        elif self.is_open():
            return "Running"
        elif now < self.start_time():
            return "Scheduled"
        else:
            return "Closed"

    def __str__(self):
        return f"Auction for {self.pearl.name}"
    


class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.auction.is_open():
            raise ValidationError("Cannot bid: auction is not open.")
        
        if self.bidder == self.auction.pearl.owner:
            raise ValidationError("You cannot bid on your own pearl.")
        
        min_required = self.auction.get_min_next_bid()

        if self.amount < min_required:
            raise ValidationError(f"Your bid must be at least {min_required}.")
        

    def save(self, *args, **kwargs):
        is_create = self.pk is None
        if is_create:
            self.full_clean()

            self.auction.last_bid_time = timezone.now()
            self.auction.save(update_fields=['last_bid_time'])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bidder.username} bid {self.amount} on {self.auction.pearl.name}"

    