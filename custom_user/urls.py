from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('login',LoginView.as_view(), name= "login"),
    path('logout', Logout.as_view() , name="logout"),
    path("signup", Signup.as_view(), name="signup"),
    path('verify_otp', Verify_otp.as_view(), name='verify_otp'),
    path('shipping-adr', ShippingAddressView.as_view(), name="shipadr"),
    
   
]
