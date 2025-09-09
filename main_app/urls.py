from django.urls import path
from .views import HomePageView, SignUpView, PearlCreateView, PearlListView, PearlDetailView, PearlUpdateView, PearlDeleteView, CertificationCreateView, CertificationDetailView,CertificationUpdateView,CertificationDeleteView,AuctionCreateView, AuctionUpdateView, AuctionDeleteView, AuctionListView, AuctionDetailView, ProfileDetailView, ProfileUpdateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("auth/signup/",SignUpView.as_view(), name="signup"),

    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="profile"),
    path("profile/<int:pk>/edit/", ProfileUpdateView.as_view(), name="profile_edit"),


    path('auth/logout/', LogoutView.as_view(next_page='home'), name='logout'),


    # Pearl URL
    path("pearls/", PearlListView.as_view(), name="pearl_list"),
    path("pearls/<int:pk>/", PearlDetailView.as_view(), name="pearl_detail"),
    path("pearls/create/", PearlCreateView.as_view(), name="pearl_create"),
    path("pearls/<int:pk>/update/", PearlUpdateView.as_view(), name="pearl_update"),
    path("pearls/<int:pk>/delete/", PearlDeleteView.as_view(), name="pearl_delete"),


    # Certification URL
     path('pearls/<int:pk>/certifications/add/', CertificationCreateView.as_view(), name='certification_create'),
     path('certifications/<int:pk>/edit/', CertificationUpdateView.as_view(), name='certification_update'),
     path('certifications/<int:pk>/', 
     CertificationDetailView.as_view(), name='certification_detail'),
      path('certifications/<int:pk>/delete/', CertificationDeleteView.as_view(), name='certification_delete'),

      # Auction URL
     path('auction/create/<int:pk>/', AuctionCreateView.as_view(), name='auction_create'),
     path('auction/update/<int:pk>/', AuctionUpdateView.as_view(), name='auction_update'),
     path('auction/delete/<int:pk>/', AuctionDeleteView.as_view(), name='auction_delete'),
     path('auctions/', AuctionListView.as_view(), name='auction_list'),
     path('auctions/<int:pk>', AuctionDetailView.as_view(), name='auction_detail')

]
