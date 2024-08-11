from django.forms import ModelForm
from .models import AdminUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AdminForm(ModelForm):
    class Meta:
        model = AdminUser
        fields = ['company_name']


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')
