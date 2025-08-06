from django.contrib import admin
from .models import User, BloodRequest

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile', 'email')

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blood_group', 'is_available')
