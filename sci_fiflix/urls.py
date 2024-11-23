from django.urls import path
from .views import login_view, otp_verify_view
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('otp-verify/', otp_verify_view, name='otp_verify'),
   # path('', lambda request: render(request, 'home.html'), name='home'),  # Home page
]
