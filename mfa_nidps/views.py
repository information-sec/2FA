from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from .utils import send_otp
from datetime import datetime 
import pyotp
from django.contrib.auth.models import User

def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password= password)
        if user is not None:
            # send OTP
            send_otp(request)
            
            request.session['username'] = username
            return redirect('otp')
        
        else:
            error_message = 'Username or password is invalid'
            
    return render(request, 'login.html', {'error_message': error_message})

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username'] 
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_until']
        
        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)
            
            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=30)
                if totp.verify(otp):
                    user = get_object_or_404(User, username=username)
                    login(request, user)
                    
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_until']
                    
                    return redirect('main')
                    
                else:
                    error_message = 'Invalid otp'
            else:
                error_message = 'Expired otp'
        else:
            error_message = 'Something went wrong...'
                        
          
    return render(request, 'otp.html', {'error_message': error_message})


@login_required
def main_view(request):
    if 'username' in request.session:
        del request.session['username']
        
    return render(request, 'main.html')


def logout_view(request):
    logout(request)
    return redirect('login')


