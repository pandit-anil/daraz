from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('contact-us',views.Contact, name="contact"),
    path('about',AboutView.as_view(), name="about"),
]
