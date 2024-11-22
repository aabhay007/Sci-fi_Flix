from django.db import models

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
