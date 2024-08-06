from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    profile_pic = models.ImageField(upload_to='userprofile', blank=True)
    is_active = models.BooleanField(default=False)
   

    def __str__(self):
        return self.username



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    district = models.CharField(max_length=200)
    address = models.CharField(max_length=300)

    def __str__(self):
        return self.district
    
    
