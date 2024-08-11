from django.contrib import admin
from .models import UserProfile, AdminUser, EmailOtp

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(AdminUser)
admin.site.register(EmailOtp)
