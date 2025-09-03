from django.urls import path
from .views import HomePageView, ProfileView, SignUpView, PearlCreateView, PearlListView, PearlDetailView, PearlUpdateView, PearlDeleteView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),

    path("auth/signup/",SignUpView.as_view(), name="signup"),

    path("accouts/profile/", ProfileView.as_view(), name="profile"),

     path("pearls/", PearlListView.as_view(), name="pearl_list"),
    path("pearls/<int:pk>/", PearlDetailView.as_view(), name="pearl_detail"),
    path("pearls/create/", PearlCreateView.as_view(), name="pearl_create"),
    path("pearls/<int:pk>/update/", PearlUpdateView.as_view(), name="pearl_update"),
    path("pearls/<int:pk>/delete/", PearlDeleteView.as_view(), name="pearl_delete"),

]
