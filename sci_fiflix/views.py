from django.shortcuts import render, redirect
from .models import Movie
from django.contrib import messages
from .models import User, OTP
from .forms import LoginForm, OTPForm
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client

def send_otp(user):
    otp = OTP.generate_otp()
    OTP.objects.create(user=user, code=otp)

    # Send OTP via email
    if user.email:
        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}. It is valid for 5 minutes.',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

    # Send OTP via SMS (optional)
    if user.phone_number:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'Your OTP is {otp}. It is valid for 5 minutes.',
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.phone_number
        )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            user = User.objects.filter(email=identifier).first() or User.objects.filter(phone_number=identifier).first()

            if not user:
                # Register new user
                user = User.objects.create(email=identifier if '@' in identifier else None,
                                           phone_number=identifier if '@' not in identifier else None)

            send_otp(user)
            request.session['user_id'] = user.id
            return redirect('otp_verify')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def otp_verify_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp_code = form.cleaned_data['otp']
            otp = OTP.objects.filter(user=user, code=otp_code).first()

            if otp and otp.is_valid():
                messages.success(request, 'Login successful!')
                return redirect('home')  # Replace with your dashboard or home page
            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPForm()

    return render(request, 'otp_verify.html', {'form': form})

def home(request):
    trending_movies = Movie.objects.filter(is_trending=True)
    new_releases = Movie.objects.order_by('-release_date')

    context = {
        'trending_movies': trending_movies,
        'new_releases': new_releases,
    }
    return render(request, 'home.html', context)
