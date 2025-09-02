from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pearl


# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'