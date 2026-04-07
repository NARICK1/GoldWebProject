from turtle import ht
from django.shortcuts import render
from django.http import HttpResponse #короче, это удали, если хочешь, Макс, но я оставил на всякий
# Create your views here.
def home(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html' )