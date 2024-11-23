from django import forms
from .models import User

class LoginForm(forms.Form):
    identifier = forms.CharField(label='Email or Phone', max_length=100)

class OTPForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', max_length=6)
