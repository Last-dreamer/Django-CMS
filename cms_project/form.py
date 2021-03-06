from django.contrib.auth.forms import UserCreationForm, User
from django.forms import ModelForm
from .models import Order, Customer


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'


class Customer_Profile(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user']
