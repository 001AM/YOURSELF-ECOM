from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = "home"),
    path('store/', views.store, name='store'),
    path('store/<str:pk>/<str:pk1>',views.store, name = "store"),
    path('store/<str:pk>',views.store, name = "store"),
    path('product/<str:pk>/',views.product, name = "product"),
    path('search',views.search, name = "search"),
    path('register',views.register,name="register"),
    path('login/',views.loginUser, name = "login"),
    path('logout/',views.logoutUser, name = "logout"),
    path('userprofile/',views.userprofile, name = "userprofile"),
    path('userprofile/contactus',views.contactus, name = "contactus"),
    path('userprofile/logout',views.proflogout, name = "proflogout"),
    path('userprofile/order',views.order, name = "order"),
    path('add_to_cart/<str:prod_name>/',views.add_to_cart, name = "addtocart"),
    path('cart/',views.cart, name = "cart"),
    path('remove_from_cart/<str:cart_item_id>/',views.remove_from_cart, name = "remove_from_cart"),
    path('payment/',views.payment, name = "payment"),
    path('paymentfailure/',views.paymentfailure, name = "paymentfailure"),
    path('invoice/<str:q>/',views.invoice, name = "invoice"),
]
