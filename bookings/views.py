from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Booking
from .forms import BookingForm


def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save()
                # Send confirmation email if email provided
                if booking.email:
                    try:
                        send_mail(
                            subject='Appointment Confirmed ✅',
                            message=f"""
Dear {booking.customer_name},

Your appointment has been confirmed!

Service: {booking.service.name}
Date: {booking.date}
Time: {booking.time}
Status: {booking.status}

Thank you for booking with us!
                            """,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[booking.email],
                            fail_silently=True,
                        )
                    except Exception:
                        pass
                return redirect('booking_success')
            except Exception as e:
                messages.error(request, str(e))
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = BookingForm()

    return render(request, 'bookings/booking.html', {'form': form})


def booking_success(request):
    return render(request, 'bookings/success.html')


def get_available_slots(request):
    """AJAX endpoint - returns booked slots for a date"""
    from django.http import JsonResponse
    date = request.GET.get('date')
    if date:
        booked = Booking.objects.filter(
            date=date,
            status__in=['Pending', 'Confirmed']
        ).values_list('time', flat=True)
        booked_list = [str(t)[:5] for t in booked]
        return JsonResponse({'booked': booked_list})
    return JsonResponse({'booked': []})
