from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count
import datetime
from bookings.models import Booking
from services.models import Service
from chatbot.models import BusinessKnowledge


@login_required
def dashboard_home(request):
    today = datetime.date.today()

    # Stats
    total_bookings = Booking.objects.count()
    today_bookings = Booking.objects.filter(date=today).count()
    pending = Booking.objects.filter(status='Pending').count()
    confirmed = Booking.objects.filter(status='Confirmed').count()

    # Recent bookings
    recent = Booking.objects.select_related('service').order_by('-created_at')[:10]

    # Today's appointments
    todays = Booking.objects.filter(date=today).select_related('service').order_by('time')

    context = {
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'pending': pending,
        'confirmed': confirmed,
        'recent_bookings': recent,
        'todays_appointments': todays,
        'today': today,
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def all_bookings(request):
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')

    bookings = Booking.objects.select_related('service').order_by('-date', '-time')

    if status_filter:
        bookings = bookings.filter(status=status_filter)
    if date_filter:
        bookings = bookings.filter(date=date_filter)

    return render(request, 'dashboard/bookings.html', {
        'bookings': bookings,
        'status_filter': status_filter,
        'date_filter': date_filter,
    })


@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save(update_fields=['status'])
            messages.success(request, f'Booking #{booking.id} status updated to {new_status}')
    return redirect('all_bookings')


@login_required
def knowledge_base(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            BusinessKnowledge.objects.create(title=title, content=content)
            messages.success(request, 'Knowledge added successfully!')
        return redirect('knowledge_base')

    knowledge = BusinessKnowledge.objects.all().order_by('-created_at')
    return render(request, 'dashboard/knowledge.html', {'knowledge': knowledge})


@login_required
def delete_knowledge(request, pk):
    item = get_object_or_404(BusinessKnowledge, pk=pk)
    item.delete()
    messages.success(request, 'Deleted successfully.')
    return redirect('knowledge_base')


@login_required
def manage_services(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        duration = request.POST.get('duration', 60)
        price = request.POST.get('price')
        if name and price:
            Service.objects.create(name=name, description=description, duration=duration, price=price)
            messages.success(request, f'Service "{name}" added!')
        return redirect('manage_services')

    services = Service.objects.all()
    return render(request, 'dashboard/services.html', {'services': services})
