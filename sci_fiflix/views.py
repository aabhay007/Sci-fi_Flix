from django.shortcuts import render, redirect
from .models import Movie
from django.contrib import messages
from .models import User, OTP
from .forms import LoginForm, OTPForm
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password

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
            is_email = '@' in identifier

            # Fetch user by email or phone number
            user = User.objects.filter(email=identifier if is_email else None).first() or \
                   User.objects.filter(phone_number=identifier if not is_email else None).first()

            if not user:
                # Create a partially registered user
                user = User.objects.create(
                    email=identifier if is_email else None,
                    phone_number=identifier if not is_email else None
                )

            # Save the identifier in the session for OTP verification
            request.session['user_id'] = user.id
            request.session['identifier'] = identifier
            send_otp(user)
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
                # Log the user in
                login(request, user)  # This is critical for maintaining the session
                messages.success(request, 'Login successful!')
                return redirect('home')

            else:
                messages.error(request, 'Invalid or expired OTP.')
    else:
        form = OTPForm()

    return render(request, 'otp_verify.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')

def home(request):
    trending_movies = Movie.objects.filter(is_trending=True)
    new_releases = Movie.objects.order_by('-release_date')

    context = {
        'trending_movies': trending_movies,
        'new_releases': new_releases,
        'user': request.user,  # Pass the user to the template
        'is_authenticated': request.user.is_authenticated,  # Check if the user is logged in
    }

    # Debugging logs (optional, for development)
    print(f"User: {request.user}")
    print(f"Is Authenticated: {request.user.is_authenticated}")

    return render(request, 'home.html', context)

