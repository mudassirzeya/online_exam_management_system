from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# sending email
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .tokens import random_with_N_digits
from django.conf import settings
import json
from .models import AdminUser, EmailOtp, UserProfile
from .forms import AdminForm, RegisterForm
from .password import PasswordSet
from django.http import JsonResponse

# reset password
from django.http import HttpResponse
# from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.auth.models import User
# from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
# from django.core.mail import EmailMultiAlternatives
from django.core.mail import BadHeaderError
from django import template
import time
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        # user = request.user

        if user is not None:
            login(request, user)
            staffProfile = UserProfile.objects.get(user=request.user)
            usertype = staffProfile.user_type
            print("request.user: ", request.user)
            if usertype == 'admin':
                return redirect('admin_page')
            elif usertype == 'staff':
                # print("user page")
                return redirect('staff_page')
            elif usertype == 'student':
                return redirect('student_home')
            else:
                messages.info(request, 'Username or Password is in correct')
        else:
            messages.info(request, 'Username or Password is in correct')
    context = {}
    return render(request, 'login_page.html', context)


def sendOtp(request):
    form1 = RegisterForm()
    form2 = AdminForm()

    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['data_obj'][0].get('email')
        otp = random_with_N_digits()
        try:
            otp_table = EmailOtp.objects.get(email=email)
            otp_table.delete()
        except:
            pass
        try:
            existing_user = User.objects.get(email=email)
            print(existing_user)
            return JsonResponse({"msg": "Error"})
        except:
            pass
        # if existing_email is False:
        EmailOtp.objects.create(
            email=email,
            otp=otp,
        )

        msg_html = render_to_string('email_otp.html',
                                    {'email': email, 'otp': otp})
        text_content = strip_tags(msg_html)

        email = EmailMultiAlternatives(
            # title
            'Email Authentication OTP',

            # context
            text_content,

            # from email
            settings.EMAIL_HOST_USER,

            # to email
            [email],
        )
        email.attach_alternative(msg_html, "text/html")
        email.send()

        return JsonResponse({"msg": "success"})
    else:
        context = {"form1": form1, "form2": form2}
        return render(request, 'signup_page.html', context)


def otp_verify(request):
    form1 = RegisterForm()
    form2 = AdminForm()
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['data_obj'][0].get('email')
        otp = data['data_obj'][0].get('otp')
        # print("OTP:", otp, " ", "email:", email)
        email_otp_backend = EmailOtp.objects.get(email=email)
        if email_otp_backend.otp == otp:
            print("success")
            EmailOtp.objects.get(
                email=email,
                otp=otp
            ).delete()
            return JsonResponse({"msg": "success"})
        else:
            print("fail")
            return JsonResponse({"msg": "fail"})
    context = {"form1": form1, "form2": form2}
    return render(request, 'signup_page.html', context)


def staff_signup(request):
    form1 = RegisterForm()
    form2 = AdminForm()
    if request.method == 'POST':
        form1 = RegisterForm(request.POST)
        form2 = AdminForm(request.POST)
        username = request.POST.get('email')
        if form1.is_valid():
            new_user = form1.save(commit=False)
            new_user.username = username
            new_user.save()
            if form2.is_valid():
                admin_obj = form2.save(commit=False)
                admin_obj.user = new_user
                admin_obj.save()
                UserProfile.objects.create(
                    user=new_user,
                    user_type='admin',
                )
                return redirect('login')
    context = {'form1': form1, 'form2': form2}
    return render(request, 'signup_page.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


def password_reset_request(request):
    if request.method == "POST":
        data = request.POST.get('email')
        # if password_reset_form.is_valid():
        # data = password_reset_form.cleaned_data['email']
        associated_users = User.objects.filter(
            Q(email=data) | Q(username=data))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                plaintext = template.loader.get_template(
                    'password_reset_email.txt')
                htmltemp = template.loader.get_template(
                    'password_reset_email.html')
                c = {
                    "email": user.email,
                    'domain': '127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                text_content = plaintext.render(c)
                html_content = htmltemp.render(c)
                try:
                    msg = EmailMultiAlternatives(subject, text_content, 'Website <influence1405@gmail.com>', [
                        user.email], headers={'Reply-To': 'mudassirzeya206@gmail.com'})
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.info(
                    request, "Password reset instructions have been sent to the email address entered.")
                return redirect("password_reset_done")
        else:
            messages.info(request, 'Invalid Username')
    # password_reset_form = PasswordResetForm()
    return render(request=request, template_name="staff_login.html", context={"password_reset_form": "Invalid Username"})


def add_new_staff(request):
    loggedin_user = AdminUser.objects.get(user=request.user)
    company = loggedin_user.company_name
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        passcode = PasswordSet()
        try:
            exist_user = User.objects.get(username=email)
        except Exception:
            exist_user = None
        if not exist_user:
            new_user = User.objects.create_user(
                username=email, password=passcode)
            new_user.email = email
            new_user.first_name = name
            new_user.save()
            UserProfile.objects.create(
                user=new_user,
                company_assign=loggedin_user,
                user_type='staff',
            )

            msg_html = render_to_string('add_staff_email.html',
                                        {'first_name': name, 'Institution': company, 'username': email, 'password': passcode})
            text_content = strip_tags(msg_html)

            email = EmailMultiAlternatives(
                # title
                f'Mail From {company} admin',

                # context
                text_content,

                # from email
                settings.EMAIL_HOST_USER,

                # to email
                [email],
            )
            email.attach_alternative(msg_html, "text/html")
            email.send()
            messages.info(request, 'User Create Successfully!')
        else:
            messages.info(request, 'User already exists')
        return redirect('admin_page')

    context = {}
    return render(request, 'admin_page.html', context)


def logout_student(request):
    if request.method == 'POST':
        logout(request)
        time.sleep(2)
        return JsonResponse({'msg': 'success'})
    return render(request, 'login_page.html')
