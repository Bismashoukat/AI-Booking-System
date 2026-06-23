from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('bookings/', views.all_bookings, name='all_bookings'),
    path('bookings/<int:booking_id>/status/', views.update_booking_status, name='update_status'),
    path('knowledge/', views.knowledge_base, name='knowledge_base'),
    path('knowledge/<int:pk>/delete/', views.delete_knowledge, name='delete_knowledge'),
    path('services/', views.manage_services, name='manage_services'),
]
