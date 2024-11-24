from django import forms
from .models import User

class LoginForm(forms.Form):
    identifier = forms.EmailField(label='', max_length=100)

class OTPForm(forms.Form):
    otp = forms.CharField(label='', max_length=6)
