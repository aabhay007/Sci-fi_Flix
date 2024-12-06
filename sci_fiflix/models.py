from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, password=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError('The user must have a phone number or email address.')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number=None, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with the given phone number, email, and password.
        """
        if not email:
            raise ValueError('Superusers must have an email address')
        if not password:
            raise ValueError('Superusers must have a password')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(phone_number=phone_number, email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    is_staff = models.BooleanField(default=False)  # Admin access
    is_active = models.BooleanField(default=True)  # Active status

    USERNAME_FIELD = 'email'  # Email is used as the username field
    REQUIRED_FIELDS = ['phone_number']  # 'email' is removed from here

    objects = UserManager()

    def __str__(self):
        return self.email or self.phone_number
class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        from datetime import timedelta
        from django.utils.timezone import now
        return now() - self.created_at < timedelta(minutes=5)

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    category = models.ForeignKey(Category, related_name='movies', on_delete=models.CASCADE)
    is_trending = models.BooleanField(default=False)
    release_date = models.DateField()

    def __str__(self):
        return self.title
