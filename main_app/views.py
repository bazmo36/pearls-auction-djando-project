from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Pearl, Certification, AuctionListing
from .forms import PearlForm, CertificationForm, BidForm
from django.utils import timezone
from django.core.exceptions import ValidationError



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

        return Pearl.objects.filter(owner=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['owner'] = context['pearls'][0].owner
        return context
    

    


# Pearl CBV

class PearlListView(LoginRequiredMixin, ListView):
    model = Pearl
    template_name = "pearls/pearl_list.html"
    context_object_name = "pearls"






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

class CertificationDetailView(LoginRequiredMixin, DetailView):
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
    fields = ['reserve_price']
    template_name = 'auction/auction_form.html'

    def dispatch(self, request, *args, **kwargs):

        self.pearl = get_object_or_404(Pearl, pk=kwargs['pk'])

        if hasattr(self.pearl, 'auction'):
            return self.handle_no_permission()
        
        if self.pearl.owner != request.user:
            return self.handle_no_permission()
        
        return super().dispatch(request, *args, **kwargs) 
    
    
    def form_valid(self, form):
        form.instance.pearl = self.pearl
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('pearl_detail', kwargs={'pk': self.pearl.pk})
    


class AuctionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AuctionListing
    fields = ['reserve_price']
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
    

class AuctionListView(TemplateView, LoginRequiredMixin):
    model = AuctionListing
    template_name = 'auction/auction_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        now = timezone.now()

        all_auctions = AuctionListing.objects.select_related('pearl')

        active_auctions = []
        upcoming_auctions = []
        closed_auctions = []

        for auction in all_auctions:
            start = auction.start_time()
            end = auction.end_time()

            if start <= now <= end:
                active_auctions.append(auction)
            elif now < start:
                upcoming_auctions.append(auction)
            else:
                closed_auctions.append(auction)

        context['active_auctions'] = active_auctions
        context['upcoming_auctions'] = upcoming_auctions
        context['closed_auctions'] = closed_auctions

        return context
    
class AuctionDetailView(LoginRequiredMixin, DetailView, FormView):
    model = AuctionListing
    template_name = 'auction/auction_detail.html'
    form_class = BidForm

    def get_object(self):
        pearl_pk = self.kwargs.get('pk')
        return AuctionListing.objects.get(pearl__pk=pearl_pk)

    def get_success_url(self):
        return self.request.path

    def get_form_kwargs(self):
       
        kwargs = super().get_form_kwargs()
        kwargs['auction'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        auction = self.get_object()

      
        if not auction.is_open():
            form.add_error(None, "Auction is not open.")
            return self.form_invalid(form)
        
        if auction.pearl.owner == self.request.user:
            form.add_error(None, "You cannot bid on your own pearl.")
            return self.form_invalid(form)


        bid = form.save(commit=False)
        bid.auction = auction
        bid.bidder = self.request.user
        
        try:
            bid.save()
        except ValidationError as err:
            errors = err.message_dict if hasattr(err, 'message_dict') else err.messages

            if isinstance(errors, dict):
                for field, msgs in errors.items():
                    for msg in msgs:
                        form.add_error(field if field != "__all__" else None, msg)
            else:
                for msg in errors:
                    form.add_error(None, msg)
            return self.form_invalid(form)

        return super().form_valid(form)



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        auction = self.get_object()

        context['current_price'] = auction.current_price()
        context['min_next_bid'] = auction.get_min_next_bid()
        context['bid_history'] = auction.bids.order_by('-amount')[:10] 
        context['now'] = timezone.now() 
        return context
