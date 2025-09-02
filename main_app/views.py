from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pearl
from .forms import PearlForm


# Create your views here.

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'


# Pearl CBV

class PearlListView(LoginRequiredMixin, ListView):
    model = Pearl
    template_name = "pearls/pearl_list.html"

    def get_queryset(self):
        return Pearl.objects.filter(owner=self.request.user)


class PearlDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Pearl
    template_name = "pearls/pearl_detail.html"

    def test_func(self):
        pearl = self.get_object()
        return pearl.owner == self.request.user
    

class PearlCreateView(LoginRequiredMixin, CreateView):
    model = Pearl
    form_class = PearlForm
    template_name = "pearls/pearl_form.html"


class PearlUpdateView(LoginRequiredMixin, UpdateView):
    model = Pearl
    form_class = PearlForm
    template_name = "pearls/pearl_form.html"
    

