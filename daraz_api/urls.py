from django.urls import path,include
from . views import *
from rest_framework import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'',CategoryViewCRUD)

urlpatterns = [
    path('',include(router.urls)),
    path('category', CategoryView.as_view())
]
