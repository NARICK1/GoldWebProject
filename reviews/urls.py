from django.urls import path
from . import views

urlpatterns = [
    path('', views.reviews_list, name='reviews_list'),
    path('add/', views.add_review, name='add_review'),  
]