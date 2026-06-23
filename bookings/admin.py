from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'service', 'date', 'time', 'status', 'phone']
    list_filter = ['status', 'date', 'service']
    search_fields = ['customer_name', 'phone', 'email']
    list_editable = ['status']
    ordering = ['-date', '-time']
