from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_booking, name='booking'),
    path('success/', views.booking_success, name='booking_success'),
    path('slots/', views.get_available_slots, name='available_slots'),
]
