from django.contrib import admin
from . models import *
from ckeditor.widgets import CKEditorWidget
from django.db import models

class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget()},
    }

admin.site.register(Product, ProductAdmin)

admin.site.register(Advertise)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)

