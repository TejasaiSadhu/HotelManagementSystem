from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.urls import reverse, reverse_lazy
# from .models import Room  

# Create your views here.

def ProfileView(request):
    return render(request, 'profile_view.html')

def MainView(request):
    return render(request, 'main_view.html')