from django import forms
from .models import Booking
from services.models import Service
import datetime


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking
        fields = ['customer_name', 'phone', 'email', 'service', 'date', 'time']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your Full Name'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+92 300 0000000'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'your@email.com (optional)'
            }),
            'service': forms.Select(attrs={
                'class': 'form-input'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input',
                'min': str(datetime.date.today())
            }),
            'time': forms.Select(attrs={
                'class': 'form-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        selected_date = kwargs.pop('selected_date', None)
        super().__init__(*args, **kwargs)

        # Available time slots
        all_slots = [
            ('10:00', '10:00 AM'),
            ('11:00', '11:00 AM'),
            ('12:00', '12:00 PM'),
            ('13:00', '01:00 PM'),
            ('14:00', '02:00 PM'),
            ('15:00', '03:00 PM'),
            ('16:00', '04:00 PM'),
            ('17:00', '05:00 PM'),
            ('18:00', '06:00 PM'),
        ]
        self.fields['time'] = forms.ChoiceField(
            choices=[('', 'Select Time')] + all_slots,
            widget=forms.Select(attrs={'class': 'form-input'})
        )
        self.fields['service'].queryset = Service.objects.filter(is_active=True)
        self.fields['service'].empty_label = "Select Service"
