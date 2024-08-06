from django.contrib import admin
from .models import SystemSystem

class SystemSystemAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_num', 'address')  # Fields to display in the list view
    search_fields = ('name', 'email')  # Fields to search in the admin interface
    list_filter = ('address',)  # Filters to apply on the list view
    readonly_fields = ('email',)  # Fields that should be read-only

admin.site.register(SystemSystem, SystemSystemAdmin)
