from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class CustomUser(UserAdmin):
        fieldsets = (
            (None, {"fields": ("username","email", "mobile_number","profile_pic", "password")}),
            ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
            )
        add_fieldsets = (
            (None, {
                "classes": ("wide",),
                "fields": (
                    "username", "email", "mobile_number", "profile_pic","password","is_staff",
                    "is_active", "groups", "user_permissions"
                )}
                ),
             )
        
admin.site.register(ShippingAddress)