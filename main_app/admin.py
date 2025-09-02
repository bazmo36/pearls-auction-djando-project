from django.contrib import admin
from .models import Pearl, Certification, AuctionListing, Bid


# Register your models here.


admin.site.register(Pearl)
admin.site.register(AuctionListing)
admin.site.register(Bid)
admin.site.register(Certification)
