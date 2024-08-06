from django.urls import path
from .views import *
from . import views

urlpatterns = [
    
    path('', IndexView.as_view(),name="index"),
    path('details/<int:id>', views.DetailView,name="details"),
    path('add-cart/<int:id>',views.AddOrder, name="cart"),
    path('cart-view',views.OrderView, name="cartview"),
    path('remove-order/<int:order_id>',Remove_Order.as_view(), name="remove"),
    path('increase/<int:order_id>',views.increase_quantity, name="incre"),
    path('decrease/<int:order_id>',views.decrease_quantity, name="decre"),
    path('payment', PaymentView.as_view(),name="payment"),
    path('category/<int:id>', CategoryBasedView.as_view(), name="category"),
    path('review/<int:id>', ReviewView.as_view(), name="review"),

]

