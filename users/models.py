from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class AdminUser(models.Model):
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    company_logo = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True,)

    def __str__(self):
        return str(self.user)


class UserProfile(models.Model):
    USERTYPE = (
        ('student', 'student'),
        ('staff', 'staff'),
        ('admin', 'admin'),
    )
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    company_assign = models.ForeignKey(
        AdminUser, null=True, blank=True, on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(
        default="profile1.jpg", null=True, blank=True)
    user_type = models.CharField(max_length=100, blank=True, choices=USERTYPE)
    date_of_joining = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class EmailOtp(models.Model):
    email = models.CharField(max_length=100, blank=True)
    otp = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.email)
