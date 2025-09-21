from django.contrib import admin
from .models import Pearl, Certification, AuctionListing, Bid, Profile


# Register your models here.

admin.site.register(Profile)
admin.site.register(Pearl)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Certification)
