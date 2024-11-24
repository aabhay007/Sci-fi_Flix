from django.contrib import admin
from .models import Category, Movie, User

admin.site.register(Category)
admin.site.register(Movie)
admin.site.register(User)