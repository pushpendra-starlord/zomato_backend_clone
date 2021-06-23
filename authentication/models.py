from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    USER_TYPE = (
        (1 , "User"),
        (2 , "Seller"),
        (3, "Dilevery Boy")
    )
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    user_category = models.PositiveSmallIntegerField(choices=USER_TYPE, default=1)
    profile_image = models.ImageField(upload_to = 'profile_image', default = 'profile_image/default_image.png')
    phone = models.CharField(max_length=10, unique=True, blank=True, null=True)
    otp_code = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
