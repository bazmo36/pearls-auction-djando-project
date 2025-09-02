from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta



# Create your models here.


class Pearl(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pearls")
    name= models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="pearls/",blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (owned by {self.owner.username})"
    


class Certification(models.Model):
    pearl = models.OneToOneField(Pearl, on_delete=models.CASCADE, related_name="certification")
    certified_by = models.CharField(max_length=100)
    certificate_number = models.CharField(max_length=50, unique=True)
    grade = models.CharField(max_length=50)
    issued_at = models.DateField()

    def __str__(self):
        return f"Certificate {self.certificate_number} for {self.pearl.name}"
    



class AuctionListing(models.Model):
    pearl = models.OneToOneField("Pearl", on_delete=models.CASCADE, related_name="auction")
    starting_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)  

    def start_time(self):
        created_date = self.created_at
        days_ahead = 0 - created_date.weekday()  # 0 = Monday
        if days_ahead <= 0:
            days_ahead += 7
        next_monday = (created_date + timedelta(days=days_ahead)).replace(
        hour=0, minute=0, second=0)
        return next_monday

    def end_time(self):
        start = self.start_time()
        return start.replace(hour=23, minute=59, second=59)

    def is_open(self):
        now = timezone.now()
        return self.start_time() <= now <= self.end_time()


    

class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        if self.amount <= self.auction.current_price:
            raise ValueError("Bid must be higher than current price")
        super().save(*args, **kwargs)

    
    def __str__(self):
      return f"{self.bidder.username} bid {self.amount} on {self.auction.pearl.name}"
