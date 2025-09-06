from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pearl, Certification, AuctionListing
from .forms import PearlForm, CertificationForm


# Create your views here.

class HomePageView(ListView):
    model = Pearl
    template_name = "home.html"
    context_object_name = "pearls"
    ordering = ["-created_at"]

class SignUpView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = 'registration/signup.html'


class ProfileView(LoginRequiredMixin, ListView):
    model = Pearl
    template_name = "profile.html"
    context_object_name = "pearls"

    
    def get_queryset(self):
        return Pearl.objects.filter(owner=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    




# Pearl CBV

class PearlListView(LoginRequiredMixin, ListView):
    model = Pearl
    template_name = "pearls/pearl_list.html"
    context_object_name = "pearls"

    def pearl_list(request):
        pearls = Pearl.objects.all()  # fetch all pearls from all users
        return render(request, 'pearl_list.html', {'pearls': pearls})




class PearlDetailView(LoginRequiredMixin, DetailView):
    model = Pearl
    template_name = "pearls/pearl_detail.html"
    



    

class PearlCreateView(LoginRequiredMixin, CreateView):
    model = Pearl
    form_class = PearlForm
    template_name = "pearls/pearl_form.html"
    success_url = reverse_lazy('pearl_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PearlUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Pearl
    form_class = PearlForm
    template_name = "pearls/pearl_form.html"
    success_url = reverse_lazy('pearl_list')

    
    def test_func(self):
        pearl = self.get_object()
        return self.request.user == pearl.owner


    
class PearlDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Pearl
    success_url = reverse_lazy('pearl_list')

    def test_func(self):
        pearl = self.get_object()
        return self.request.user == pearl.owner


# CBV Certification 

class CertificationDetailView(LoginRequiredMixin, DeleteView):
    model = Certification
    template_name = 'certifications/certification_detail.html'
    context_object_name = 'certification'
    
class CertificationCreateView(CreateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'certifications/certification_form.html'

    def dispatch(self, request, *args, **kwargs):

        self.pearl = get_object_or_404(Pearl, pk=kwargs['pk'])

        if self.pearl.owner != request.user:
            return HttpResponseForbidden("You do not have the permission to certify this pearl.")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.pearl = self.pearl
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['pearl'] =self.pearl
        return context
    
    def get_success_url(self):
        return reverse('pearl_detail', kwargs={'pk': self.pearl.pk})


class CertificationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certification
    form_class = CertificationForm
    template_name = 'certifications/certification_form.html'

    def get_success_url(self):
        return reverse('pearl_detail', kwargs={'pk': self.object.pearl.pk})

    def test_func(self):
        certification = self.get_object()
        return certification.pearl.owner == self.request.user


class CertificationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certification
    
    def get_success_url(self):
        return reverse_lazy('pearl_detail', kwargs={'pk': self.object.pearl.pk})

    def test_func(self):
        certification = self.get_object()
        return certification.pearl.owner == self.request.user
    

class AuctionCreateView(LoginRequiredMixin, CreateView):
    model = AuctionListing
    fields = ['starting_price']
    template_name = 'auction/auction_form.html'

    def dispatch(self, request, *args, **kwargs):

        self.pearl = get_object_or_404(Pearl, pk=kwargs['pk'])

        if hasattr(self.pearl, 'auction'):
            return self.handle_no_permission
        
        if self.pearl.owner != request.user:
            return self.handle_no_permission
        
        return super().dispatch(request, *args, **kwargs) 
    
    def form_valid(self, form):
        form.instance.pearl = self.pearl
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pearl_detail', kwargs={'pk': self.pearl.pk})
    


class AuctionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AuctionListing
    fields = ['starting_price']
    template_name = 'auction/auction_form.html'

    def test_func(self):
        auction = self.get_object()
        return self.request.user == auction.pearl.owner and auction.can_modify()
    
    def get_success_url(self):
        return reverse_lazy('pearl_detail', kwargs={'pk': self.object.pearl.pk})

class AuctionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AuctionListing

    def test_func(self):
        auction = self.get_object()
        return self.request.user == auction.pearl.owner and auction.can_modify()
    
    def get_success_url(self):
        return reverse_lazy('pearl_detail', kwargs={'pk': self.object.pearl.pk})
    

    