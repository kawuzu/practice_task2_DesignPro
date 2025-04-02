from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)



class Request(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='request_photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Новая')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)