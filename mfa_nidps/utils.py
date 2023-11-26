import pyotp
from datetime import datetime, timedelta

def send_otp(request):
    # Generate random secret
    totp = pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp = totp.now() # The otp that should be inputted by the user
    
    request.session['otp_secret_key'] = totp.secret  # store the secret key in the user session
     
    # set expiration time for the otp
    valid_until = datetime.now() + timedelta(minutes=1)
    
    request.session['otp_valid_until'] = str(valid_until) 
    
    print(f"Your one time password is: {otp}")
    
    
    
    
    

