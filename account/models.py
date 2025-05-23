from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Custom_User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    otp = models.PositiveIntegerField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics/', default='def.png', blank=True, null=True)

    def __str__(self):
        return self.username