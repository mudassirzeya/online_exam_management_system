from django.urls import path
from .views import login_page, staff_signup, sendOtp, otp_verify, logout_user, password_reset_request, add_new_staff, logout_student
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', login_page, name='login'),
    path('staff_signup/', staff_signup, name='staff_signup'),
    path('logout/', logout_user, name='logout'),
    path('email_auth/', sendOtp, name='email_auth'),
    path('otp_verify/', otp_verify, name='otp_verify'),
    path('reset', password_reset_request, name='reset'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="staff_login.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_confirm/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="password_reset_done.html"),
         name="password_reset_complete"),
    path('add_new_staff', add_new_staff, name='add_new_staff'),
    path('logout_student/', logout_student, name='logout_student'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
