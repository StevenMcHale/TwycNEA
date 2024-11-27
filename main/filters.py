import django_filters
from .models import *

class BookingFilter(django_filters.FilterSet):
    class Meta:
        model = Booking
        fields = '__all__'
        exclude = ['date_created', 'booking_id']

