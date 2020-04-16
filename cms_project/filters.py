import django_filters
from .models import Order


class filter_order(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer']
