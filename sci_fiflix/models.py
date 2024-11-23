from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import random

class UserManager(BaseUserManager):
    def create_user(self, phone_number=None, email=None, **extra_fields):
        if not phone_number and not email:
            raise ValueError('The user must have a phone number or email address.')
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)

    USERNAME_FIELD = 'email'
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
