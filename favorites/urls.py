from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorites_view, name='favorites'),
    path('add/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
]