from django.db import models
from ckeditor.fields import RichTextField
from custom_user.models import User

class SystemSystem(models.Model):
    name = models.CharField(max_length=100)
    mobile_num = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=150, blank=True)
    email = models.EmailField()
    logo = models.ImageField(upload_to='sysLogo', blank=True)
    image = models.ImageField(upload_to='sysimg', blank=True)
    about = RichTextField()
    slogan = RichTextField()
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = "System"
        verbose_name_plural = "Systems"
        ordering = ['name']  # Default ordering of records
        db_table = 'system_system'  # Custom table name if needed
    
    def __str__(self):
        return self.name
    
class ContactUs(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contactuss')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.customer.name   