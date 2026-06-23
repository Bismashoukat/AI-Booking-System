from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/chatbot/', permanent=False)),
    path('services/', include('services.urls')),
    path('bookings/', include('bookings.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
]
