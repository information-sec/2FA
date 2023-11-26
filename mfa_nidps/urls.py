"""
URL configuration for mfa_nidps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import login_view, otp_view, main_view, logout_view

from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.models import User

class OTPAdmin(OTPAdminSite):
    pass

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice)


urlpatterns = [
    path('admin/', admin_site.urls),
    path('traditional-admin/', admin.site.urls),
    path('', main_view, name='main'),
    path('login/', login_view, name='login'),
    path('login/otp/', otp_view, name='otp'),
    path('logout/', logout_view, name='logout'),
]
