from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .decorators import isUserAuthenticated, allowed_users, adminOnly
from .form import CreateUserForm, OrderForm, Customer_Profile
from .models import Product, Customer, Order
from .filters import filter_order


@isUserAuthenticated
def register(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
                name=user.username
            )

    context = {'form': form}
    return render(request, 'cms_project/register.html', context)


@isUserAuthenticated
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {}
    return render(request, 'cms_project/login.html', context)


@login_required(login_url='login')
def Logout(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@adminOnly
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_orders = orders.count()
    pending = orders.filter(status='pending').count()
    delivered = orders.filter(status='delivered').count()

    context = {'customers': customers,
               'orders': orders,
               'total_orders': total_orders,
               'pending': pending,
               'delivered': delivered
               }
    return render(request, 'cms_project/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_user=['admin'])
def product(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'cms_project/product.html', context)


def userPage(request, pk):
    current_user = Customer.objects.get(id=pk)
    orders = current_user.order_set.all()
    total_orders = orders.count()
    pending = orders.filter(status='pending').count()
    delivered = orders.filter(status='delivered').count()
    context = {'current_user': current_user,
               'orders': orders,
               'total_orders': total_orders,
               'pending': pending,
               'delivered': delivered}
    return render(request, 'cms_project/user_page.html', context)


@login_required(login_url='login')
@allowed_users(allowed_user=['admin'])
def customer(request, pk):
    # getting the current user as a Customer.....
    customers = Customer.objects.get(id=pk)
    # to get child's of  another model we  user its name with _set like from Order  i.e order_set 
    order = customers.order_set.all()

    # for search  ... filter_order is own class model which extends from django_filters,,,,
    orderFilter = filter_order(request.GET, queryset=order)
    order = orderFilter.qs
    
    total_orders = order.count()
    context = {'customers': customers,
               'total_orders': total_orders,
               'order': order,
               'orderFilter': orderFilter
               }
    return render(request, 'cms_project/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_user=['admin'])
def createOrder(request, pk):
    #  for multiple forms to submit at a time ..
    # extra  will be number of forms
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)

    current_customer = Customer.objects.get(id=pk)
    form_set = orderFormSet(queryset=Order.objects.none(), instance=current_customer)

    # for single form 
    # orderForm = Or derForm
    if request.method == 'POST':
        form_set = orderFormSet(request.POST, instance=current_customer)
        # orderForm = OrderForm(request.POST)
        if form_set.is_valid():
            form_set.save()
            return redirect('/customer/'+str(current_customer.id))
    context = {'form_set': form_set}
    return render(request, 'cms_project/orderPage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_user=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    orderForm = OrderForm(instance=order)
    if request.method == 'POST':
        orderForm = OrderForm(request.POST, instance=order)
        if orderForm.is_valid():
            orderForm.save()
            return redirect('/')
    context = {'form_set': orderForm}
    return render(request, 'cms_project/orderPage.html', context)


@login_required(login_url='login')
@allowed_users(allowed_user=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'cms_project/deletePage.html', context)


def setting(request):
    # it will get the current customer...
    current_user = request.user.customer
    profile = Customer_Profile(instance=current_user)
    if request.method == 'POST':
        profile = Customer_Profile(request.POST, request.FILES, instance=current_user)
        if profile.is_valid():
            profile.save()
            return redirect('/')

    context = {'profile': profile}
    return render(request, 'cms_project/user_setting.html', context)
