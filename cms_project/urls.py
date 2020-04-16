from . import views
from django.urls import path

urlpatterns = [
    path('register', views.register, name="register"),
    path('login', views.Login, name="login"),
    path('logout', views.Logout, name="logout"),
    path('', views.home, name="home"),
    path('product/', views.product, name='product'),
    path('customer/<str:pk>', views.customer, name='customer'),
    path('create_order/<str:pk>', views.createOrder, name="create_order"),
    path('update_order/<str:pk>', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>', views.deleteOrder, name="delete_order"),
    path('user_page/<str:pk>', views.userPage, name="user_page"),
    path('setting', views.setting, name="setting"),
]
